"""Skill System - Skill definition and execution"""

import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from agently.logging import get_logger

logger = get_logger(__name__)


@dataclass
class SkillStep:
    """
    Skill Step - 技能步骤

    定义技能执行的一个步骤。
    """

    name: str
    description: str
    action: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    condition: Optional[str] = None
    on_failure: str = "stop"  # stop, continue, retry

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "action": self.action,
            "parameters": self.parameters,
            "condition": self.condition,
            "on_failure": self.on_failure,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkillStep":
        """Create from dictionary"""
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            action=data.get("action", ""),
            parameters=data.get("parameters", {}),
            condition=data.get("condition"),
            on_failure=data.get("on_failure", "stop"),
        )


@dataclass
class SkillResult:
    """
    Skill Result - 技能执行结果

    包含技能执行的完整结果信息。
    """

    success: bool
    output: Any = None
    error: Optional[str] = None
    step_results: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Skill:
    """
    Skill - 技能

    定义一个可执行的技能，包含多个步骤。
    """

    name: str
    description: str
    steps: List[SkillStep]
    version: str = "1.0"
    author: str = ""
    tags: List[str] = field(default_factory=list)
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate skill definition"""
        if not self.name:
            return False
        if not self.steps:
            return False
        for step in self.steps:
            if not step.name or not step.action:
                return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "tags": self.tags,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "steps": [step.to_dict() for step in self.steps],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Skill":
        """Create from dictionary"""
        steps = [SkillStep.from_dict(s) for s in data.get("steps", [])]
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            version=data.get("version", "1.0"),
            author=data.get("author", ""),
            tags=data.get("tags", []),
            inputs=data.get("inputs", {}),
            outputs=data.get("outputs", {}),
            steps=steps,
        )

    @classmethod
    def from_yaml(cls, path: Path) -> "Skill":
        """Load skill from YAML file"""
        content = path.read_text()
        data = yaml.safe_load(content)
        return cls.from_dict(data)

    def to_yaml(self, path: Path) -> None:
        """Save skill to YAML file"""
        content = yaml.dump(self.to_dict(), default_flow_style=False)
        path.write_text(content)


class SkillRegistry:
    """
    Skill Registry - 技能注册表

    管理所有可用技能的注册和查找。
    """

    def __init__(self):
        self._skills: Dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        """Register a skill"""
        if not skill.validate():
            raise ValueError(f"Invalid skill: {skill.name}")
        self._skills[skill.name] = skill
        logger.info("Skill registered", skill=skill.name)

    def unregister(self, name: str) -> None:
        """Unregister a skill"""
        if name in self._skills:
            del self._skills[name]

    def get(self, name: str) -> Optional[Skill]:
        """Get a skill by name"""
        return self._skills.get(name)

    def list_skills(self) -> List[str]:
        """List all registered skill names"""
        return list(self._skills.keys())

    def get_all(self) -> List[Skill]:
        """Get all registered skills"""
        return list(self._skills.values())

    def load_from_directory(self, directory: Path) -> int:
        """
        Load skills from a directory

        Args:
            directory: Directory containing skill YAML files

        Returns:
            Number of skills loaded
        """
        count = 0
        for path in directory.glob("**/*.yaml"):
            try:
                skill = Skill.from_yaml(path)
                self.register(skill)
                count += 1
            except Exception as e:
                logger.warning("Failed to load skill", path=str(path), error=str(e))

        for path in directory.glob("**/*.yml"):
            try:
                skill = Skill.from_yaml(path)
                self.register(skill)
                count += 1
            except Exception as e:
                logger.warning("Failed to load skill", path=str(path), error=str(e))

        logger.info("Skills loaded from directory", directory=str(directory), count=count)
        return count

    def clear(self) -> None:
        """Clear all registered skills"""
        self._skills.clear()


class SkillExecutor:
    """
    Skill Executor - 技能执行器

    执行技能并管理执行上下文。
    """

    def __init__(
        self,
        skill_registry: Optional[SkillRegistry] = None,
        agent_executor: Optional[Callable] = None,
    ):
        self.skill_registry = skill_registry or SkillRegistry()
        self.agent_executor = agent_executor
        self.execution_history: List[Dict[str, Any]] = []

    def execute(
        self,
        skill_name: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> SkillResult:
        """
        Execute a skill

        Args:
            skill_name: Name of the skill to execute
            context: Execution context

        Returns:
            Skill execution result
        """
        skill = self.skill_registry.get(skill_name)

        if skill is None:
            return SkillResult(
                success=False,
                error=f"Skill '{skill_name}' not found",
            )

        context = context or {}
        step_results = []

        logger.info("Executing skill", skill=skill_name, steps=len(skill.steps))

        for i, step in enumerate(skill.steps):
            try:
                # Merge step parameters with context
                step_context = {**context, **step.parameters}

                # Execute step via agent executor
                if self.agent_executor:
                    step_result = self.agent_executor(
                        agent_name=step.action,
                        context=step_context,
                    )
                else:
                    # Mock execution for testing
                    step_result = {"result": f"Executed {step.name}"}

                step_results.append({
                    "step": step.name,
                    "action": step.action,
                    "result": step_result,
                    "success": True,
                })

                # Update context with step result
                context.update(step_result)

            except Exception as e:
                step_results.append({
                    "step": step.name,
                    "action": step.action,
                    "error": str(e),
                    "success": False,
                })

                if step.on_failure == "stop":
                    return SkillResult(
                        success=False,
                        error=f"Step '{step.name}' failed: {e}",
                        step_results=step_results,
                    )
                elif step.on_failure == "continue":
                    continue
                elif step.on_failure == "retry":
                    # Simple retry once
                    try:
                        if self.agent_executor:
                            step_result = self.agent_executor(
                                agent_name=step.action,
                                context=step_context,
                            )
                        else:
                            step_result = {"result": f"Retried {step.name}"}

                        step_results[-1] = {
                            "step": step.name,
                            "action": step.action,
                            "result": step_result,
                            "success": True,
                        }
                    except Exception as retry_error:
                        return SkillResult(
                            success=False,
                            error=f"Step '{step.name}' failed after retry: {retry_error}",
                            step_results=step_results,
                        )

        # Record execution
        self.execution_history.append({
            "skill": skill_name,
            "context": context,
            "success": True,
            "steps": len(step_results),
        })

        return SkillResult(
            success=True,
            output=context,
            step_results=step_results,
        )

    def get_history(self) -> List[Dict[str, Any]]:
        """Get execution history"""
        return self.execution_history.copy()

    def clear_history(self) -> None:
        """Clear execution history"""
        self.execution_history.clear()


# Built-in skills
def get_builtin_skills() -> List[Skill]:
    """Get list of built-in skills"""
    return [
        Skill(
            name="code-generation",
            description="Generate code from requirements",
            tags=["code", "generation"],
            steps=[
                SkillStep(
                    name="understand",
                    description="Understand requirements",
                    action="code-understander",
                ),
                SkillStep(
                    name="generate",
                    description="Generate code",
                    action="code-generator",
                ),
                SkillStep(
                    name="review",
                    description="Review generated code",
                    action="code-reviewer",
                ),
            ],
        ),
        Skill(
            name="bug-fixing",
            description="Fix bugs in code",
            tags=["bug", "fix"],
            steps=[
                SkillStep(
                    name="analyze",
                    description="Analyze the bug",
                    action="bug-fixer",
                ),
                SkillStep(
                    name="fix",
                    description="Apply fix",
                    action="bug-fixer",
                ),
                SkillStep(
                    name="test",
                    description="Verify fix",
                    action="tester",
                ),
            ],
        ),
        Skill(
            name="code-review",
            description="Review code for issues",
            tags=["review", "quality"],
            steps=[
                SkillStep(
                    name="analyze",
                    description="Analyze code structure",
                    action="code-understander",
                ),
                SkillStep(
                    name="review",
                    description="Review for issues",
                    action="code-reviewer",
                ),
            ],
        ),
    ]


def create_default_skill_registry() -> SkillRegistry:
    """Create registry with built-in skills"""
    registry = SkillRegistry()
    for skill in get_builtin_skills():
        registry.register(skill)
    return registry
