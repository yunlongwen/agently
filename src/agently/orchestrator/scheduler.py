"""Agent Scheduler - Schedules agent execution"""

from typing import Any, Dict, List, Optional

from agently.agents.base import BaseAgent


class AgentScheduler:
    """
    Agent Scheduler - 智能体调度器

    负责任务调度、资源分配、并发控制和超时管理。
    """

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.execution_queue: List[Dict[str, Any]] = []
        self.running_tasks: Dict[str, Any] = {}
        self.max_concurrent: int = 3

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent for scheduling"""
        self.agents[agent.name] = agent

    def schedule_agent(
        self,
        capability: str,
        task_context: Dict[str, Any]
    ) -> Optional[BaseAgent]:
        """
        Schedule an agent based on capability requirement

        Args:
            capability: Required capability
            task_context: Task context

        Returns:
            Selected agent or None
        """
        # Find agents with matching capability
        candidates = [
            agent for agent in self.agents.values()
            if agent.can_handle(capability)
        ]

        if not candidates:
            return None

        # Select best agent based on load and performance
        selected = self._select_best_agent(candidates)
        return selected

    def _select_best_agent(self, candidates: List[BaseAgent]) -> BaseAgent:
        """Select the best agent from candidates"""
        # For now, return the first available
        # In production, consider:
        # - Current load
        # - Historical performance
        # - Cost
        # - Latency
        return candidates[0]

    def queue_task(self, task: Dict[str, Any]) -> str:
        """Add task to execution queue"""
        task_id = f"task_{len(self.execution_queue)}"
        task["id"] = task_id
        task["status"] = "queued"
        self.execution_queue.append(task)
        return task_id

    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Get next task from queue"""
        if not self.execution_queue:
            return None

        # Check concurrent limit
        if len(self.running_tasks) >= self.max_concurrent:
            return None

        task = self.execution_queue.pop(0)
        task["status"] = "running"
        self.running_tasks[task["id"]] = task

        return task

    def complete_task(self, task_id: str, result: Dict[str, Any]) -> None:
        """Mark task as complete"""
        if task_id in self.running_tasks:
            del self.running_tasks[task_id]

    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        return {
            "queued": len(self.execution_queue),
            "running": len(self.running_tasks),
            "max_concurrent": self.max_concurrent,
        }

    def set_max_concurrent(self, max_concurrent: int) -> None:
        """Set maximum concurrent tasks"""
        self.max_concurrent = max(1, max_concurrent)
