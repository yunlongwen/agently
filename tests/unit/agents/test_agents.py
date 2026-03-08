"""Tests for agents layer"""

from unittest.mock import Mock, patch

from agently.agents.base import AgentContext, AgentResult, BaseAgent
from agently.agents.nexus import NexusAgent
from agently.agents.specialist import (
    BugFixerAgent,
    CodeGeneratorAgent,
    CodeReviewerAgent,
    CodeUnderstandingAgent,
    GitManagerAgent,
    QualityAssuranceAgent,
    RequirementsAnalyzerAgent,
)


class ConcreteTestAgent(BaseAgent):
    """Concrete agent for testing BaseAgent"""

    def execute(self, context: AgentContext) -> AgentResult:
        return AgentResult(success=True, data={"test": True})


class TestBaseAgent:
    """Test BaseAgent class"""

    def test_base_agent_init(self):
        """Test initializing base agent"""
        agent = ConcreteTestAgent(name="test-agent", description="Test agent")
        assert agent.name == "test-agent"
        assert agent.description == "Test agent"
        assert agent.capabilities == []


class TestAgentContext:
    """Test AgentContext class"""

    def test_context_init(self):
        """Test initializing agent context"""
        context = AgentContext(task="test task")
        assert context.task == "test task"
        assert context.context == {}
        assert context.history == []

    def test_context_with_data(self):
        """Test context with additional data"""
        context = AgentContext(task="test task", context={"key": "value"}, history=[{"step": 1}])
        assert context.context["key"] == "value"
        assert len(context.history) == 1


class TestAgentResult:
    """Test AgentResult class"""

    def test_result_init(self):
        """Test initializing agent result"""
        result = AgentResult(success=True, data={"output": "test"})
        assert result.success is True
        assert result.data["output"] == "test"
        assert result.error is None

    def test_result_failure(self):
        """Test failed result"""
        result = AgentResult(success=False, error="Something went wrong")
        assert result.success is False
        assert result.error == "Something went wrong"


class TestNexusAgent:
    """Test NexusAgent class"""

    def test_nexus_init(self):
        """Test initializing Nexus agent"""
        nexus = NexusAgent()
        assert nexus.name == "nexus"
        assert "综合" in nexus.description

    def test_nexus_register_agent(self):
        """Test registering agents with Nexus"""
        nexus = NexusAgent()
        mock_agent = Mock(spec=BaseAgent)
        mock_agent.name = "test-agent"
        mock_agent.capabilities = ["test"]

        nexus.register_agent(mock_agent)
        assert "test-agent" in nexus.agents

    def test_nexus_execute_delegates_to_specialist(self):
        """Test Nexus delegates to specialist agent"""
        nexus = NexusAgent()
        mock_agent = Mock(spec=BaseAgent)
        mock_agent.name = "code-generator"
        mock_agent.capabilities = ["code-generation"]
        mock_agent.execute.return_value = AgentResult(success=True, data={"code": "test"})

        nexus.register_agent(mock_agent)

        context = AgentContext(task="generate code for test")
        with patch.object(nexus, "_select_agent", return_value=mock_agent):
            result = nexus.execute(context)

        assert result.success is True


class TestRequirementsAnalyzerAgent:
    """Test RequirementsAnalyzerAgent"""

    def test_init(self):
        """Test initializing requirements analyzer"""
        agent = RequirementsAnalyzerAgent()
        assert agent.name == "requirements-analyzer"
        assert "需求" in agent.description

    def test_execute(self):
        """Test executing requirements analysis"""
        agent = RequirementsAnalyzerAgent()
        context = AgentContext(task="analyze requirements for login feature")
        with patch.object(agent, "_analyze", return_value={"requirements": ["req1"]}):
            result = agent.execute(context)

        assert isinstance(result, AgentResult)


class TestRequirementsAnalyzerAgentReal:
    """Test RequirementsAnalyzerAgent with real requirements analysis"""

    def test_analyze_user_requirements(self):
        """Test that RequirementsAnalyzerAgent analyzes user requirements"""
        agent = RequirementsAnalyzerAgent()
        context = AgentContext(task="实现用户登录功能，包括邮箱和密码验证")
        result = agent.execute(context)
        assert result.success is True
        analysis = result.data
        requirements = analysis["requirements"]

        # Should have extracted functional requirements, not just as task string
        assert isinstance(requirements, list)
        assert len(requirements) > 0

        # Check that requirements are extracted, not full task string
        for req in requirements:
            # Should not just be the full task string
            assert len(req) < len(context.task) if not req.startswith("[") else True

        # Should contain key functional keywords
        assert any(
            keyword in " ".join(requirements) for keyword in ["登录", "邮箱", "密码", "验证"]
        )

    def test_analyze_empty_requirements(self):
        """Test that RequirementsAnalyzerAgent handles empty requirements"""
        agent = RequirementsAnalyzerAgent()
        context = AgentContext(task="")
        result = agent.execute(context)
        assert result.success is True
        analysis = result.data
        requirements = analysis["requirements"]
        assert len(requirements) == 0

    def test_analyze_vague_requirements(self):
        """Test that RequirementsAnalyzerAgent identifies vague requirements"""
        agent = RequirementsAnalyzerAgent()
        context = AgentContext(task="做一些事情")
        result = agent.execute(context)
        assert result.success is True
        analysis = result.data
        requirements = analysis["requirements"]

        # Should mark as vague and ask for clarification
        assert len(requirements) > 0
        assert any(
            "澄清" in req or "不明确" in req or "模糊" in req or "vague" in req.lower()
            for req in requirements
        )


class TestCodeGeneratorAgentReal:
    """Test CodeGeneratorAgent with real code generation"""

    def test_generate_function_code(self):
        """Test that CodeGeneratorAgent generates function code"""
        agent = CodeGeneratorAgent()
        context = AgentContext(task="写一个函数，实现两个数相加")
        result = agent.execute(context)
        assert result.success is True
        generated = result.data
        assert "code" in generated
        assert "+" in generated["code"] and "add" in generated["code"]

    def test_generate_empty_task(self):
        """Test CodeGeneratorAgent handles empty task"""
        agent = CodeGeneratorAgent()
        context = AgentContext(task="")
        result = agent.execute(context)
        assert result.success is True
        generated = result.data
        assert "code" in generated
        assert generated["code"] != ""

    def test_generate_generates_valid_python(self):
        """Test that generated code is valid Python"""
        agent = CodeGeneratorAgent()
        context = AgentContext(task="生成一个函数")
        result = agent.execute(context)
        assert result.success is True
        generated = result.data
        assert "code" in generated
        # Should have function definition syntax
        assert "def " in generated["code"]
        # Should have parameters
        assert "(" in generated["code"]
        assert ")" in generated["code"]
        assert ":" in generated["code"]
        # Should have return statement
        assert "return " in generated["code"]


class TestCodeUnderstandingAgentReal:
    """Test CodeUnderstandingAgent"""

    def test_init(self):
        """Test initializing code understanding agent"""
        agent = CodeUnderstandingAgent()
        assert agent.name == "code-understander"
        assert "代码理解" in agent.description


class TestBugFixerAgentReal:
    """Test BugFixerAgent"""

    def test_init(self):
        """Test initializing bug fixer agent"""
        agent = BugFixerAgent()
        assert agent.name == "bug-fixer"
        assert "调试" in agent.description


class TestQualityAssuranceAgent:
    """Test QualityAssuranceAgent"""

    def test_init(self):
        """Test initializing tester agent"""
        agent = QualityAssuranceAgent()
        assert agent.name == "tester"
        assert "测试" in agent.description


class TestCodeReviewerAgentReal:
    """Test CodeReviewerAgent"""

    def test_init(self):
        """Test initializing code reviewer agent"""
        agent = CodeReviewerAgent()
        assert agent.name == "code-reviewer"
        assert "审查" in agent.description


class TestGitManagerAgentReal:
    """Test GitManagerAgent"""

    def test_init(self):
        """Test initializing git manager agent"""
        agent = GitManagerAgent()
        assert agent.name == "git-manager"
        assert "Git" in agent.description
