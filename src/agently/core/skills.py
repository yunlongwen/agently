"""Skill system for defining and executing complex workflows"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
import yaml


@dataclass
class SkillStep:
    """A single step in a skill"""
    name: str
    description: str
    action: str
    parameters: Optional[Dict[str, Any]] = None


@dataclass
class SkillResult:
    """Result of skill execution"""
    success: bool
    output: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    step_results: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Skill:
    """A skill composed of multiple steps"""
    name: str
    description: str
    steps: List[SkillStep] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Skill":
        """Create skill from dictionary

        Args:
            data: Skill definition

        Returns:
            Skill instance
        """
        steps = [
            SkillStep(
                name=step["name"],
                description=step["description"],
                action=step["action"],
                parameters=step.get("parameters"),
            )
            for step in data.get("steps", [])
        ]
        return cls(
            name=data["name"],
            description=data["description"],
            steps=steps,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert skill to dictionary

        Returns:
            Skill as dictionary
        """
        return {
            "name": self.name,
            "description": self.description,
            "steps": [
                {
                    "name": step.name,
                    "description": step.description,
                    "action": step.action,
                    "parameters": step.parameters,
                }
                for step in self.steps
            ],
        }

    def validate(self) -> bool:
        """Validate skill definition

        Returns:
            True if valid
        """
        return len(self.steps) > 0


class SkillRegistry:
    """Registry for skills"""

    def __init__(self):
        self._skills: Dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        """Register a skill

        Args:
            skill: Skill to register
        """
        self._skills[skill.name] = skill

    def get(self, name: str) -> Optional[Skill]:
        """Get a skill by name

        Args:
            name: Skill name

        Returns:
            Skill or None
        """
        return self._skills.get(name)

    def list_skills(self) -> List[str]:
        """List all registered skills

        Returns:
            List of skill names
        """
        return list(self._skills.keys())

    def load_from_directory(self, directory: Path) -> None:
        """Load skills from YAML files in directory

        Args:
            directory: Directory containing skill files
        """
        for file_path in directory.glob("*.yaml"):
            with file_path.open() as f:
                data = yaml.safe_load(f)
                if data:
                    skill = Skill.from_dict(data)
                    self.register(skill)


class SkillExecutor:
    """Executes skills"""

    def __init__(
        self,
        skill_registry: SkillRegistry,
        agent_executor: Callable,
    ):
        self.skill_registry = skill_registry
        self.agent_executor = agent_executor

    def execute(
        self, skill_name: str, context: Optional[Dict[str, Any]] = None
    ) -> SkillResult:
        """Execute a skill

        Args:
            skill_name: Name of skill to execute
            context: Execution context

        Returns:
            Execution result
        """
        skill = self.skill_registry.get(skill_name)
        if skill is None:
            return SkillResult(
                success=False,
                error=f"Skill '{skill_name}' not found",
            )

        context = context or {}
        step_results = []

        try:
            for step in skill.steps:
                result = self._execute_step(step, context)
                step_results.append(result)
                context.update(result)

            return SkillResult(
                success=True,
                output=context,
                step_results=step_results,
            )
        except Exception as e:
            return SkillResult(
                success=False,
                error=str(e),
                step_results=step_results,
            )

    def _execute_step(
        self, step: SkillStep, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a single step

        Args:
            step: Step to execute
            context: Current context

        Returns:
            Step result
        """
        params = step.parameters or {}
        params.update(context)
        return self.agent_executor(step.action, params)
