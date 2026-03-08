"""Multi-Agent Collaboration Integration Tests

Tests for multi-agent collaboration workflows.
Following TDD: tests are written before implementation.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CollaborationState:
    """State for multi-agent collaboration"""

    task: str
    agent_history: list[dict[str, Any]] = field(default_factory=list)
    current_agent: str = ""
    result: str = ""
    is_complete: bool = False


class TestMultiAgentCollaboration:
    """Test multi-agent collaboration workflows"""

    def test_agent_registry_integration(self):
        """RED: Test that agents can be registered and retrieved"""
        from agently.agents.base import AgentContext, AgentResult, BaseAgent
        from agently.orchestrator.nexus import NexusOrchestrator

        # Create a test agent
        class TestAgent(BaseAgent):
            def __init__(self):
                super().__init__(
                    name="test-agent",
                    description="Test agent for collaboration",
                    capabilities=["test"],
                )

            def execute(self, context: AgentContext) -> AgentResult:
                return AgentResult(
                    success=True,
                    data={"agent": self.name, "task": context.task},
                )

        # Create orchestrator and register agent
        orchestrator = NexusOrchestrator()
        orchestrator.nexus.register_agent(TestAgent())

        # Execute through nexus
        result = orchestrator.nexus.execute(AgentContext(task="test task with test capability"))

        assert result.success is True
        assert result.data["agent"] == "test-agent"

    def test_sequential_agent_handoff(self):
        """RED: Test sequential handoff between agents"""
        from agently.agents.base import AgentContext, AgentResult, BaseAgent

        # Create agents that pass work between each other
        class AnalyzerAgent(BaseAgent):
            def __init__(self):
                super().__init__(
                    name="analyzer",
                    description="Analyzes tasks",
                    capabilities=["analyze"],
                )

            def execute(self, context: AgentContext) -> AgentResult:
                return AgentResult(
                    success=True,
                    data={
                        "analysis": f"Analyzed: {context.task}",
                        "next_step": "plan",
                    },
                )

        class PlannerAgent(BaseAgent):
            def __init__(self):
                super().__init__(
                    name="planner",
                    description="Creates plans",
                    capabilities=["plan"],
                )

            def execute(self, context: AgentContext) -> AgentResult:
                return AgentResult(
                    success=True,
                    data={
                        "plan": f"Plan for: {context.task}",
                        "next_step": "execute",
                    },
                )

        class ExecutorAgent(BaseAgent):
            def __init__(self):
                super().__init__(
                    name="executor",
                    description="Executes plans",
                    capabilities=["execute"],
                )

            def execute(self, context: AgentContext) -> AgentResult:
                return AgentResult(
                    success=True,
                    data={"result": f"Executed: {context.task}"},
                )

        # Simulate sequential handoff
        context = AgentContext(task="Build a feature")

        # Analyzer runs first
        analyzer = AnalyzerAgent()
        analysis_result = analyzer.execute(context)

        # Planner runs with analysis result
        context.context.update(analysis_result.data)
        planner = PlannerAgent()
        plan_result = planner.execute(context)

        # Executor runs with plan
        context.context.update(plan_result.data)
        executor = ExecutorAgent()
        final_result = executor.execute(context)

        assert "Analyzed:" in analysis_result.data["analysis"]
        assert "Plan for:" in plan_result.data["plan"]
        assert "Executed:" in final_result.data["result"]

    def test_parallel_agent_execution(self):
        """RED: Test parallel execution of multiple agents"""
        import concurrent.futures

        from agently.agents.base import AgentContext, AgentResult, BaseAgent

        class ReviewAgent(BaseAgent):
            def __init__(self, focus: str):
                super().__init__(
                    name=f"reviewer-{focus}",
                    description=f"Reviews {focus}",
                    capabilities=["review"],
                )
                self.focus = focus

            def execute(self, context: AgentContext) -> AgentResult:
                return AgentResult(
                    success=True,
                    data={self.focus: f"Reviewed {self.focus} of {context.task}"},
                )

        # Create multiple reviewers
        reviewers = [
            ReviewAgent("code_quality"),
            ReviewAgent("security"),
            ReviewAgent("performance"),
        ]

        context = AgentContext(task="Review this PR")

        # Execute in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(reviewer.execute, context) for reviewer in reviewers]
            results = [f.result() for f in futures]

        # Verify all reviewers ran
        assert len(results) == 3
        assert any("code_quality" in str(r.data) for r in results)
        assert any("security" in str(r.data) for r in results)
        assert any("performance" in str(r.data) for r in results)

    def test_agent_collaboration_with_shared_state(self):
        """RED: Test agents collaborating with shared state"""
        from agently.agents.base import AgentContext, AgentResult, BaseAgent

        class SharedStateAgent(BaseAgent):
            def __init__(self, name: str, capability: str, modification: str):
                super().__init__(name=name, description=name, capabilities=[capability])
                self.modification = modification

            def execute(self, context: AgentContext) -> AgentResult:
                # Read shared state
                shared_data = context.context.get("shared_data", [])
                # Modify shared state
                shared_data.append(f"{self.name}: {self.modification}")
                context.context["shared_data"] = shared_data

                return AgentResult(
                    success=True,
                    data={"shared_data": shared_data},
                )

        # Create agents that modify shared state
        context = AgentContext(task="Collaborative task", context={"shared_data": []})

        agents = [
            SharedStateAgent("agent1", "step1", "completed step 1"),
            SharedStateAgent("agent2", "step2", "completed step 2"),
            SharedStateAgent("agent3", "step3", "completed step 3"),
        ]

        # Execute sequentially, passing shared state
        for agent in agents:
            result = agent.execute(context)
            context.context.update(result.data)

        # Verify shared state accumulated correctly
        final_state = context.context["shared_data"]
        assert len(final_state) == 3
        assert "agent1: completed step 1" in final_state
        assert "agent2: completed step 2" in final_state
        assert "agent3: completed step 3" in final_state

    def test_agent_orchestration_with_nexus(self):
        """RED: Test full orchestration using Nexus"""
        from agently.agents.base import AgentContext, AgentResult, BaseAgent
        from agently.agents.nexus import NexusAgent

        class CodeAgent(BaseAgent):
            def __init__(self):
                super().__init__(
                    name="code-specialist",
                    description="Code generation specialist",
                    capabilities=["code", "programming"],
                )

            def execute(self, context: AgentContext) -> AgentResult:
                return AgentResult(
                    success=True,
                    data={"code": f"# Code for: {context.task}"},
                )

        class TestAgent(BaseAgent):
            def __init__(self):
                super().__init__(
                    name="test-specialist",
                    description="Testing specialist",
                    capabilities=["test", "testing"],
                )

            def execute(self, context: AgentContext) -> AgentResult:
                return AgentResult(
                    success=True,
                    data={"tests": f"# Tests for: {context.task}"},
                )

        # Create nexus and register specialists
        nexus = NexusAgent()
        nexus.register_agent(CodeAgent())
        nexus.register_agent(TestAgent())

        # Execute code task
        code_context = AgentContext(task="Write code to sort a list")
        code_result = nexus.execute(code_context)

        assert code_result.success is True
        assert "code" in code_result.data or "Code" in str(code_result.data)

        # Execute test task
        test_context = AgentContext(task="Write tests for the sorting function")
        test_result = nexus.execute(test_context)

        assert test_result.success is True
        assert "test" in str(test_result.data).lower()

    def test_agent_error_handling_in_collaboration(self):
        """RED: Test error handling when agent fails"""
        from agently.agents.base import AgentContext, AgentResult, BaseAgent

        class FailingAgent(BaseAgent):
            def __init__(self):
                super().__init__(
                    name="failing-agent",
                    description="Agent that fails",
                    capabilities=["fail"],
                )

            def execute(self, context: AgentContext) -> AgentResult:
                return AgentResult(
                    success=False,
                    error="Simulated failure",
                )

        class FallbackAgent(BaseAgent):
            def __init__(self):
                super().__init__(
                    name="fallback-agent",
                    description="Fallback agent",
                    capabilities=["fallback"],
                )

            def execute(self, context: AgentContext) -> AgentResult:
                return AgentResult(
                    success=True,
                    data={"fallback": "Handled by fallback"},
                )

        # Try failing agent first
        context = AgentContext(task="Test error handling")
        failing = FailingAgent()
        result = failing.execute(context)

        # Handle failure with fallback
        if not result.success:
            fallback = FallbackAgent()
            result = fallback.execute(context)

        assert result.success is True
        assert "fallback" in result.data

    def test_agent_capability_routing(self):
        """RED: Test routing based on agent capabilities"""
        from agently.agents.base import BaseAgent

        def select_agent_by_capability(task: str, agents: dict[str, BaseAgent]) -> BaseAgent:
            """Select agent based on task keywords matching capabilities"""
            task_lower = task.lower()
            # Find best match by counting capability occurrences
            best_match = None
            best_score = 0

            for _, agent in agents.items():
                score = sum(1 for cap in agent.capabilities if cap.lower() in task_lower)
                if score > best_score:
                    best_score = score
                    best_match = agent

            # Default to first agent if no match
            return best_match or list(agents.values())[0]

        agents = {
            "coder": BaseAgent(
                name="coder", description="Coder", capabilities=["code", "programming"]
            ),
            "writer": BaseAgent(
                name="writer", description="Writer", capabilities=["write", "documentation"]
            ),
            "tester": BaseAgent(name="tester", description="Tester", capabilities=["test", "qa"]),
        }

        # Test routing
        code_agent = select_agent_by_capability("Write code for API", agents)
        assert code_agent.name == "coder"

        doc_agent = select_agent_by_capability("Write documentation", agents)
        assert doc_agent.name == "writer"

        test_agent = select_agent_by_capability("Write tests for QA", agents)
        assert test_agent.name == "tester"
