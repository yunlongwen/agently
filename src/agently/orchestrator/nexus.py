"""Nexus orchestrator - main orchestrator implementation"""

from typing import Any, Dict

from agently.agents.base import AgentContext, AgentResult
from agently.agents.nexus import NexusAgent
from agently.orchestrator.planner import TaskPlanner
from agently.orchestrator.scheduler import AgentScheduler
from agently.orchestrator.state import StateManager
from agently.orchestrator.workflow import WorkflowEngine


class NexusOrchestrator:
    """Main orchestrator that coordinates all agents and workflows"""

    def __init__(self):
        self.nexus = NexusAgent()
        self.planner = TaskPlanner()
        self.scheduler = AgentScheduler()
        self.state_manager = StateManager()
        self.workflow_engine = WorkflowEngine()

    def process_task(self, task: str) -> Dict[str, Any]:
        """Process a task through the orchestrator

        Args:
            task: Task description

        Returns:
            Processing result
        """
        result = self.nexus.execute(context=AgentContext(task=task))
        return {"success": result.success, "data": result.data, "error": result.error}
