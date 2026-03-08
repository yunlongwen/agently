"""LangGraph Integration Tests

Tests for LangGraph integration with our agent system.
Following TDD: tests are written before implementation.
"""

import pytest


class TestLangGraphIntegration:
    """Test LangGraph integration for workflow orchestration"""

    def test_langgraph_import_available(self):
        """RED: Test that langgraph can be imported"""
        # This test should fail initially if langgraph is not installed
        try:
            from langgraph.graph import END, StateGraph

            assert StateGraph is not None
            assert END is not None
        except ImportError:
            pytest.fail("langgraph is not installed")

    def test_workflow_graph_creation(self):
        """RED: Test creating a workflow graph with LangGraph"""
        # Desired behavior: Create a simple workflow graph
        from typing import Annotated, TypedDict

        from langgraph.graph import END, StateGraph
        from langgraph.graph.message import add_messages

        class WorkflowState(TypedDict):
            messages: Annotated[list, add_messages]
            current_step: str
            result: str

        # Create graph
        workflow = StateGraph(WorkflowState)

        # Add nodes
        workflow.add_node("analyze", lambda state: {"current_step": "analyze"})
        workflow.add_node("plan", lambda state: {"current_step": "plan"})
        workflow.add_node("execute", lambda state: {"current_step": "execute"})

        # Add edges
        workflow.set_entry_point("analyze")
        workflow.add_edge("analyze", "plan")
        workflow.add_edge("plan", "execute")
        workflow.add_edge("execute", END)

        # Compile
        app = workflow.compile()

        # Execute
        result = app.invoke({"messages": [], "current_step": "start", "result": ""})

        assert result["current_step"] == "execute"

    def test_agent_workflow_with_langgraph(self):
        """RED: Test agent workflow using LangGraph"""
        from typing import Annotated, TypedDict

        from langgraph.graph import END, StateGraph
        from langgraph.graph.message import add_messages

        class AgentState(TypedDict):
            task: str
            messages: Annotated[list[str], add_messages]
            agent: str
            output: str

        # Create workflow
        workflow = StateGraph(AgentState)

        # Define agent nodes
        def analyzer(state: AgentState):
            return {"agent": "analyzer", "messages": [f"Analyzing: {state['task']}"]}

        def planner(state: AgentState):
            return {"agent": "planner", "messages": state["messages"] + ["Planning steps"]}

        def executor(state: AgentState):
            return {"agent": "executor", "output": f"Executed: {state['task']}"}

        # Add nodes
        workflow.add_node("analyzer", analyzer)
        workflow.add_node("planner", planner)
        workflow.add_node("executor", executor)

        # Define flow
        workflow.set_entry_point("analyzer")
        workflow.add_edge("analyzer", "planner")
        workflow.add_edge("planner", "executor")
        workflow.add_edge("executor", END)

        app = workflow.compile()

        # Run workflow
        result = app.invoke(
            {
                "task": "Write a function to add two numbers",
                "messages": [],
                "agent": "",
                "output": "",
            }
        )

        assert result["agent"] == "executor"
        assert "Executed:" in result["output"]
        assert len(result["messages"]) >= 2

    def test_conditional_workflow(self):
        """RED: Test conditional branching in workflow"""
        from typing import Literal, TypedDict

        from langgraph.graph import END, StateGraph

        class ReviewState(TypedDict):
            code: str
            quality_score: int
            review_result: str

        def review_code(state: ReviewState):
            # Simple mock review logic
            score = 10 if "def " in state["code"] else 3
            return {"quality_score": score}

        def route_review(state: ReviewState) -> Literal["approve", "reject"]:
            if state["quality_score"] >= 5:
                return "approve"
            return "reject"

        def approve_code(state: ReviewState):
            return {"review_result": "approved"}

        def reject_code(state: ReviewState):
            return {"review_result": "rejected"}

        workflow = StateGraph(ReviewState)

        workflow.add_node("review", review_code)
        workflow.add_node("approve", approve_code)
        workflow.add_node("reject", reject_code)

        workflow.set_entry_point("review")
        workflow.add_conditional_edges(
            "review", route_review, {"approve": "approve", "reject": "reject"}
        )
        workflow.add_edge("approve", END)
        workflow.add_edge("reject", END)

        app = workflow.compile()

        # Test approval path
        result = app.invoke({"code": "def hello(): pass", "quality_score": 0, "review_result": ""})
        assert result["review_result"] == "approved"

        # Test rejection path
        result = app.invoke({"code": "bad code", "quality_score": 0, "review_result": ""})
        assert result["review_result"] == "rejected"

    def test_nexus_agent_with_langgraph(self):
        """RED: Test Nexus agent integrated with LangGraph"""
        from typing import Annotated, Literal, TypedDict

        from langgraph.graph import END, StateGraph
        from langgraph.graph.message import add_messages

        class NexusState(TypedDict):
            task: str
            selected_agent: str
            agent_output: str
            history: Annotated[list[str], add_messages]
            is_complete: bool

        # Mock specialist agents
        def select_agent(state: NexusState):
            if "code" in state["task"].lower():
                return {"selected_agent": "code-generator"}
            return {"selected_agent": "general"}

        def route_to_agent(state: NexusState) -> Literal["code_generator", "general_agent"]:
            if state.get("selected_agent") == "code-generator":
                return "code_generator"
            return "general_agent"

        def code_generator(state: NexusState):
            return {"agent_output": f"# Generated code for: {state['task']}", "is_complete": True}

        def general_agent(state: NexusState):
            return {"agent_output": f"Response for: {state['task']}", "is_complete": True}

        workflow = StateGraph(NexusState)

        workflow.add_node("select", select_agent)
        workflow.add_node("code_generator", code_generator)
        workflow.add_node("general_agent", general_agent)

        workflow.set_entry_point("select")
        workflow.add_conditional_edges(
            "select",
            route_to_agent,
            {"code_generator": "code_generator", "general_agent": "general_agent"},
        )
        workflow.add_edge("code_generator", END)
        workflow.add_edge("general_agent", END)

        app = workflow.compile()

        # Test code generation task
        result = app.invoke(
            {
                "task": "Write code to sort a list",
                "selected_agent": "",
                "agent_output": "",
                "history": [],
                "is_complete": False,
            }
        )

        assert result["selected_agent"] == "code-generator"
        assert "Generated code" in result["agent_output"]
        assert result["is_complete"] is True
