"""Tests for skill system"""

from pathlib import Path
from unittest.mock import Mock

from agently.core.skills import (
    Skill,
    SkillExecutor,
    SkillRegistry,
    SkillResult,
    SkillStep,
)


class TestSkillStep:
    """Test SkillStep"""

    def test_step_creation(self):
        """Test creating a skill step"""
        step = SkillStep(
            name="analyze",
            description="Analyze the code",
            action="code-understander",
        )
        assert step.name == "analyze"
        assert step.description == "Analyze the code"
        assert step.action == "code-understander"

    def test_step_with_parameters(self):
        """Test step with parameters"""
        step = SkillStep(
            name="generate",
            description="Generate code",
            action="code-generator",
            parameters={"language": "python", "style": "clean"},
        )
        assert step.parameters["language"] == "python"


class TestSkillResult:
    """Test SkillResult"""

    def test_success_result(self):
        """Test successful skill result"""
        result = SkillResult(success=True, output={"code": "def hello(): pass"})
        assert result.success is True
        assert result.output["code"] is not None

    def test_error_result(self):
        """Test error skill result"""
        result = SkillResult(success=False, error="Skill execution failed")
        assert result.success is False
        assert result.error == "Skill execution failed"

    def test_result_with_steps(self):
        """Test result with step results"""
        result = SkillResult(
            success=True,
            output={},
            step_results=[
                {"step": "analyze", "result": "analyzed"},
                {"step": "generate", "result": "generated"},
            ],
        )
        assert len(result.step_results) == 2


class TestSkill:
    """Test Skill"""

    def test_skill_creation(self):
        """Test creating a skill"""
        skill = Skill(
            name="code-generation",
            description="Generate code from requirements",
            steps=[
                SkillStep(
                    name="understand",
                    description="Understand requirements",
                    action="code-understander",
                ),
                SkillStep(name="generate", description="Generate code", action="code-generator"),
            ],
        )
        assert skill.name == "code-generation"
        assert len(skill.steps) == 2

    def test_skill_from_dict(self):
        """Test creating skill from dictionary"""
        data = {
            "name": "bug-fix",
            "description": "Fix bugs in code",
            "steps": [
                {
                    "name": "analyze",
                    "description": "Analyze the bug",
                    "action": "bug-fixer",
                }
            ],
        }
        skill = Skill.from_dict(data)
        assert skill.name == "bug-fix"
        assert len(skill.steps) == 1

    def test_skill_to_dict(self):
        """Test converting skill to dictionary"""
        skill = Skill(
            name="test-skill",
            description="Test",
            steps=[SkillStep(name="step1", description="Step 1", action="test")],
        )
        d = skill.to_dict()
        assert d["name"] == "test-skill"
        assert "steps" in d

    def test_skill_validation(self):
        """Test skill validation"""
        skill = Skill(
            name="valid-skill",
            description="A valid skill",
            steps=[
                SkillStep(name="step1", description="Step 1", action="agent1"),
                SkillStep(name="step2", description="Step 2", action="agent2"),
            ],
        )
        assert skill.validate() is True

    def test_invalid_skill_no_steps(self):
        """Test invalid skill with no steps"""
        skill = Skill(name="invalid-skill", description="Invalid skill", steps=[])
        assert skill.validate() is False


class TestSkillRegistry:
    """Test SkillRegistry"""

    def test_register_skill(self):
        """Test registering a skill"""
        registry = SkillRegistry()
        skill = Skill(
            name="test-skill",
            description="Test skill",
            steps=[SkillStep(name="step1", description="Step", action="test")],
        )
        registry.register(skill)
        assert "test-skill" in registry.list_skills()

    def test_get_skill(self):
        """Test getting a skill by name"""
        registry = SkillRegistry()
        skill = Skill(
            name="my-skill",
            description="My skill",
            steps=[SkillStep(name="s1", description="S1", action="a1")],
        )
        registry.register(skill)

        retrieved = registry.get("my-skill")
        assert retrieved is not None
        assert retrieved.name == "my-skill"

    def test_get_nonexistent_skill(self):
        """Test getting a skill that doesn't exist"""
        registry = SkillRegistry()
        skill = registry.get("nonexistent")
        assert skill is None

    def test_list_skills(self):
        """Test listing all skills"""
        registry = SkillRegistry()

        for i in range(3):
            skill = Skill(
                name=f"skill-{i}",
                description=f"Skill {i}",
                steps=[SkillStep(name="s", description="S", action="a")],
            )
            registry.register(skill)

        skills = registry.list_skills()
        assert len(skills) == 3

    def test_load_from_directory(self, tmp_path: Path):
        """Test loading skills from directory"""
        registry = SkillRegistry()

        # Create a skill file
        skill_file = tmp_path / "test_skill.yaml"
        skill_file.write_text("""
name: loaded-skill
description: Skill loaded from file
steps:
  - name: step1
    description: First step
    action: test-agent
""")

        registry.load_from_directory(tmp_path)
        assert "loaded-skill" in registry.list_skills()


class TestSkillExecutor:
    """Test SkillExecutor"""

    def test_execute_skill(self):
        """Test executing a skill"""
        registry = SkillRegistry()
        skill = Skill(
            name="simple-skill",
            description="Simple skill",
            steps=[SkillStep(name="step1", description="Step 1", action="test-agent")],
        )
        registry.register(skill)

        # Mock agent executor
        mock_agent_executor = Mock(return_value={"result": "done"})

        executor = SkillExecutor(skill_registry=registry, agent_executor=mock_agent_executor)

        result = executor.execute("simple-skill", context={"input": "test"})
        assert result.success is True

    def test_execute_nonexistent_skill(self):
        """Test executing a skill that doesn't exist"""
        registry = SkillRegistry()
        executor = SkillExecutor(skill_registry=registry, agent_executor=Mock())

        result = executor.execute("nonexistent")
        assert result.success is False

    def test_execute_with_context(self):
        """Test executing skill with context passing"""
        registry = SkillRegistry()
        skill = Skill(
            name="context-skill",
            description="Skill with context",
            steps=[
                SkillStep(name="s1", description="S1", action="a1"),
                SkillStep(name="s2", description="S2", action="a2"),
            ],
        )
        registry.register(skill)

        mock_executor = Mock(return_value={"result": "step_result"})
        executor = SkillExecutor(skill_registry=registry, agent_executor=mock_executor)

        result = executor.execute("context-skill", context={"initial": "data"})
        assert result.success is True

    def test_execute_step_failure(self):
        """Test skill execution when a step fails"""
        registry = SkillRegistry()
        skill = Skill(
            name="failing-skill",
            description="Skill that fails",
            steps=[SkillStep(name="fail-step", description="Will fail", action="fail-agent")],
        )
        registry.register(skill)

        def failing_executor(*args, **kwargs):
            raise Exception("Step failed")

        executor = SkillExecutor(skill_registry=registry, agent_executor=failing_executor)

        result = executor.execute("failing-skill")
        assert result.success is False
