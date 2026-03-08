"""LangGraph Workflow Integration

Integrates LangGraph with the Nexus orchestrator for workflow management.
"""

from typing import Annotated, Any, Literal

from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict

from agently.logging import get_logger

logger = get_logger(__name__)


class WorkflowState(TypedDict):
    """State for workflow execution"""

    task: str
    messages: Annotated[list[str], list.__add__]
    current_step: str
    result: str
    is_complete: bool


class LangGraphWorkflow:
    """
    LangGraph-based workflow engine

    Provides workflow orchestration using LangGraph's state machine.
    """

    def __init__(self):
        self._workflow: StateGraph | None = None
        self._app: Any | None = None
        self._nodes: dict[str, callable] = {}
        self._edges: list[tuple[str, str]] = []
        self._conditional_edges: list[tuple[str, callable, dict[str, str]]] = []

    def add_node(self, name: str, func: callable) -> "LangGraphWorkflow":
        """Add a node to the workflow

        Args:
            name: Node name
            func: Function to execute

        Returns:
            Self for chaining
        """
        self._nodes[name] = func
        logger.debug("Added workflow node", node=name)
        return self

    def add_edge(self, from_node: str, to_node: str) -> "LangGraphWorkflow":
        """Add an edge between nodes

        Args:
            from_node: Source node
            to_node: Target node

        Returns:
            Self for chaining
        """
        self._edges.append((from_node, to_node))
        logger.debug("Added workflow edge", from_node=from_node, to_node=to_node)
        return self

    def add_conditional_edge(
        self,
        from_node: str,
        condition: callable,
        mapping: dict[str, str],
    ) -> "LangGraphWorkflow":
        """Add a conditional edge

        Args:
            from_node: Source node
            condition: Function to determine next node
            mapping: Mapping of condition results to nodes

        Returns:
            Self for chaining
        """
        self._conditional_edges.append((from_node, condition, mapping))
        logger.debug(
            "Added conditional edge",
            from_node=from_node,
            mapping=mapping,
        )
        return self

    def set_entry_point(self, node: str) -> "LangGraphWorkflow":
        """Set the entry point of the workflow

        Args:
            node: Entry node name

        Returns:
            Self for chaining
        """
        self._entry_point = node
        logger.debug("Set workflow entry point", entry_point=node)
        return self

    def compile(self) -> "LangGraphWorkflow":
        """Compile the workflow

        Returns:
            Self for chaining
        """
        if self._workflow is not None:
            logger.warning("Workflow already compiled, recompiling")

        self._workflow = StateGraph(WorkflowState)

        # Add nodes
        for name, func in self._nodes.items():
            self._workflow.add_node(name, func)

        # Set entry point
        if hasattr(self, "_entry_point"):
            self._workflow.set_entry_point(self._entry_point)

        # Add edges
        for from_node, to_node in self._edges:
            self._workflow.add_edge(from_node, to_node)

        # Add conditional edges
        for from_node, condition, mapping in self._conditional_edges:
            self._workflow.add_conditional_edges(from_node, condition, mapping)

        self._app = self._workflow.compile()
        logger.info("Workflow compiled successfully")
        return self

    def execute(self, initial_state: dict[str, Any]) -> dict[str, Any]:
        """Execute the workflow

        Args:
            initial_state: Initial state dictionary

        Returns:
            Final state after execution
        """
        if self._app is None:
            raise RuntimeError("Workflow not compiled. Call compile() first.")

        logger.info("Executing workflow", task=initial_state.get("task", "unknown"))

        result = self._app.invoke(initial_state)

        logger.info(
            "Workflow execution completed",
            result_steps=len(result.get("messages", [])),
        )

        return result

    def reset(self) -> "LangGraphWorkflow":
        """Reset the workflow

        Returns:
            Self for chaining
        """
        self._workflow = None
        self._app = None
        self._nodes.clear()
        self._edges.clear()
        self._conditional_edges.clear()
        logger.debug("Workflow reset")
        return self


def create_simple_workflow() -> LangGraphWorkflow:
    """Create a simple analysis -> plan -> execute workflow

    Returns:
        Compiled workflow
    """

    def analyze(state: WorkflowState):
        return {
            "current_step": "analyze",
            "messages": state["messages"] + [f"Analyzing: {state['task']}"],
        }

    def plan(state: WorkflowState):
        return {
            "current_step": "plan",
            "messages": state["messages"] + ["Planning steps"],
        }

    def execute(state: WorkflowState):
        return {
            "current_step": "execute",
            "result": f"Executed: {state['task']}",
            "is_complete": True,
        }

    workflow = (
        LangGraphWorkflow()
        .add_node("analyze", analyze)
        .add_node("plan", plan)
        .add_node("execute", execute)
        .set_entry_point("analyze")
        .add_edge("analyze", "plan")
        .add_edge("plan", "execute")
        .compile()
    )

    return workflow


def create_conditional_workflow() -> LangGraphWorkflow:
    """Create a workflow with conditional branching

    Returns:
        Compiled workflow
    """

    def review(state: WorkflowState):
        score = 10 if "def " in state["task"] else 3
        return {
            "current_step": "review",
            "messages": state["messages"] + [f"Quality score: {score}"],
            "result": str(score),
        }

    def route_review(state: WorkflowState) -> Literal["approve", "reject"]:
        try:
            score = int(state.get("result", "0"))
            return "approve" if score >= 5 else "reject"
        except ValueError:
            return "reject"

    def approve(state: WorkflowState):
        return {
            "current_step": "approve",
            "messages": state["messages"] + ["Approved"],
            "is_complete": True,
        }

    def reject(state: WorkflowState):
        return {
            "current_step": "reject",
            "messages": state["messages"] + ["Rejected - needs improvement"],
            "is_complete": True,
        }

    workflow = (
        LangGraphWorkflow()
        .add_node("review", review)
        .add_node("approve", approve)
        .add_node("reject", reject)
        .set_entry_point("review")
        .add_conditional_edge(
            "review",
            route_review,
            {"approve": "approve", "reject": "reject"},
        )
        .add_edge("approve", END)
        .add_edge("reject", END)
        .compile()
    )

    return workflow
