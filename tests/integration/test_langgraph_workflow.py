"""Tests for LangGraph workflow integration"""

import pytest
from agently.orchestrator.langgraph_workflow import (
    LangGraphWorkflow,
    WorkflowState,
    create_conditional_workflow,
    create_simple_workflow,
)


class TestLangGraphWorkflow:
    """Test LangGraph workflow integration"""

    def test_workflow_creation(self):
        """Test creating a workflow"""
        workflow = LangGraphWorkflow()
        assert workflow is not None
        assert workflow._workflow is None
        assert workflow._app is None

    def test_add_node(self):
        """Test adding nodes to workflow"""
        workflow = LangGraphWorkflow()

        def dummy_node(state):
            return {"result": "done"}

        result = workflow.add_node("test", dummy_node)

        assert result is workflow
        assert "test" in workflow._nodes
        assert workflow._nodes["test"] == dummy_node

    def test_add_edge(self):
        """Test adding edges between nodes"""
        workflow = LangGraphWorkflow()

        result = workflow.add_edge("node1", "node2")

        assert result is workflow
        assert ("node1", "node2") in workflow._edges

    def test_add_conditional_edge(self):
        """Test adding conditional edges"""
        workflow = LangGraphWorkflow()

        def condition(state):
            return "path1"

        result = workflow.add_conditional_edge(
            "start", condition, {"path1": "node1", "path2": "node2"}
        )

        assert result is workflow
        assert len(workflow._conditional_edges) == 1
        assert workflow._conditional_edges[0][0] == "start"

    def test_set_entry_point(self):
        """Test setting workflow entry point"""
        workflow = LangGraphWorkflow()

        result = workflow.set_entry_point("start")

        assert result is workflow
        assert workflow._entry_point == "start"

    def test_compile_workflow(self):
        """Test compiling a workflow"""
        workflow = LangGraphWorkflow()

        def node1(state):
            return {"current_step": "node1"}

        def node2(state):
            return {"current_step": "node2"}

        workflow.add_node("node1", node1).add_node("node2", node2).set_entry_point(
            "node1"
        ).add_edge("node1", "node2")

        result = workflow.compile()

        assert result is workflow
        assert workflow._app is not None

    def test_execute_workflow(self):
        """Test executing a compiled workflow"""
        workflow = create_simple_workflow()

        result = workflow.execute(
            {
                "task": "Test task",
                "messages": [],
                "current_step": "",
                "result": "",
                "is_complete": False,
            }
        )

        assert result["current_step"] == "execute"
        assert result["is_complete"] is True
        assert "Test task" in result["result"]

    def test_conditional_workflow_approval_path(self):
        """Test conditional workflow - approval path"""
        workflow = create_conditional_workflow()

        result = workflow.execute(
            {
                "task": "def good_code(): pass",
                "messages": [],
                "current_step": "",
                "result": "",
                "is_complete": False,
            }
        )

        assert result["current_step"] == "approve"
        assert result["is_complete"] is True
        assert "Approved" in str(result["messages"])

    def test_conditional_workflow_rejection_path(self):
        """Test conditional workflow - rejection path"""
        workflow = create_conditional_workflow()

        result = workflow.execute(
            {
                "task": "bad code without function",
                "messages": [],
                "current_step": "",
                "result": "",
                "is_complete": False,
            }
        )

        assert result["current_step"] == "reject"
        assert result["is_complete"] is True
        assert "Rejected" in str(result["messages"])

    def test_reset_workflow(self):
        """Test resetting a workflow"""
        workflow = create_simple_workflow()

        result = workflow.reset()

        assert result is workflow
        assert workflow._workflow is None
        assert workflow._app is None
        assert len(workflow._nodes) == 0

    def test_execute_uncompiled_workflow_raises_error(self):
        """Test that executing uncompiled workflow raises error"""
        workflow = LangGraphWorkflow()

        with pytest.raises(RuntimeError, match="not compiled"):
            workflow.execute({"task": "test"})

    def test_workflow_chaining(self):
        """Test fluent interface chaining"""
        workflow = LangGraphWorkflow()

        def node(state):
            return {"step": "done"}

        # All methods should return self for chaining
        result = workflow.add_node("test", node).set_entry_point("test").add_edge("test", "end")

        assert result is workflow


class TestWorkflowState:
    """Test WorkflowState TypedDict"""

    def test_workflow_state_structure(self):
        """Test WorkflowState has required fields"""
        state: WorkflowState = {
            "task": "Test",
            "messages": ["msg1", "msg2"],
            "current_step": "step1",
            "result": "result",
            "is_complete": False,
        }

        assert state["task"] == "Test"
        assert len(state["messages"]) == 2
        assert state["is_complete"] is False
