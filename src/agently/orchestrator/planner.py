"""Task planner for orchestrator"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExecutionPlan:
    """Execution plan with tasks"""

    tasks: list[dict[str, Any]] = field(default_factory=list)
    status: str = "pending"

    def mark_complete(self) -> None:
        """Mark plan as completed"""
        self.status = "completed"


class TaskPlanner:
    """Plans task execution"""

    def create_plan(self, task: str) -> ExecutionPlan:
        """Create execution plan for task

        Args:
            task: Task description

        Returns:
            Execution plan
        """
        analysis = self._analyze_task(task)
        tasks = self._decompose_task(task, analysis)
        return ExecutionPlan(tasks=tasks)

    def _analyze_task(self, task: str) -> dict[str, Any]:
        """Analyze task complexity and type

        Args:
            task: Task description

        Returns:
            Analysis results
        """
        complexity = "low" if len(task.split()) < 10 else "high"
        task_type = "code" if "code" in task.lower() else "general"
        return {"complexity": complexity, "type": task_type}

    def _decompose_task(self, task: str, analysis: dict[str, Any]) -> list[dict[str, Any]]:
        """Decompose task into steps

        Args:
            task: Task description
            analysis: Task analysis

        Returns:
            List of task steps
        """
        return [{"step": 1, "agent": "code-generator", "task": task}]
