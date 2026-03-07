"""Tests for agents layer"""

import pytest
from unittest.mock import Mock, patch

from agently.agents.base import BaseAgent, AgentContext, AgentResult
from agently.agents.nexus import NexusAgent
from agently.agents.specialist import (
    RequirementsAnalyzerAgent,
    CodeGeneratorAgent,
    CodeUnderstandingAgent,
    BugFixerAgent,
    TesterAgent,
    CodeReviewerAgent,
    GitManagerAgent,
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

    def test_base_agent_execute(self):
        """Test that execute method works"""
        agent = ConcreteTestAgent(name="test-agent", description="Test agent")
        context = AgentContext(task="test task")
        result = agent.execute(context)
        assert result.success is True


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
        context = AgentContext(
            task="test task",
            context={"key": "value"},
            history=[{"step": 1}]
        )
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
        with patch.object(nexus, '_select_agent', return_value=mock_agent):
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

        with patch.object(agent, '_analyze', return_value={"requirements": ["req1"]}):
            result = agent.execute(context)

        assert isinstance(result, AgentResult)


class TestCodeGeneratorAgent:
    """Test CodeGeneratorAgent"""

    def test_init(self):
        """Test initializing code generator"""
        agent = CodeGeneratorAgent()
        assert agent.name == "code-generator"
        assert "代码生成" in agent.description

    def test_execute(self):
        """Test executing code generation"""
        agent = CodeGeneratorAgent()
        context = AgentContext(task="generate a function to add numbers")

        with patch.object(agent, '_generate', return_value={"code": "def add(a, b): return a + b"}):
            result = agent.execute(context)

        assert isinstance(result, AgentResult)


class TestCodeUnderstandingAgent:
    """Test CodeUnderstandingAgent"""

    def test_init(self):
        """Test initializing code understanding agent"""
        agent = CodeUnderstandingAgent()
        assert agent.name == "code-understander"
        assert "代码理解" in agent.description


class TestBugFixerAgent:
    """Test BugFixerAgent"""

    def test_init(self):
        """Test initializing bug fixer agent"""
        agent = BugFixerAgent()
        assert agent.name == "bug-fixer"
        assert "调试" in agent.description


class TestTesterAgent:
    """Test TesterAgent"""

    def test_init(self):
        """Test initializing tester agent"""
        agent = TesterAgent()
        assert agent.name == "tester"
        assert "测试" in agent.description


class TestCodeReviewerAgent:
    """Test CodeReviewerAgent"""

    def test_init(self):
        """Test initializing code reviewer agent"""
        agent = CodeReviewerAgent()
        assert agent.name == "code-reviewer"
        assert "审查" in agent.description


class TestGitManagerAgent:
    """Test GitManagerAgent"""

    def test_init(self):
        """Test initializing git manager agent"""
        agent = GitManagerAgent()
        assert agent.name == "git-manager"
        assert "Git" in agent.description
