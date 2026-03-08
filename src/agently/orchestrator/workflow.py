"""Workflow engine for orchestrator"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class WorkflowDefinition:
    """Defines a workflow"""
    steps: List[Dict[str, Any]] = field(default_factory=list)
    name: str = "default-workflow"

    def add_step(self, step: Dict[str, Any]) -> None:
        """Add a step to workflow

        Args:
            step: Step definition
        """
        self.steps.append(step)


class WorkflowEngine:
    """Executes workflows"""

    def execute(self, workflow: WorkflowDefinition) -> Dict[str, Any]:
        """Execute a workflow

        Args:
            workflow: Workflow to execute

        Returns:
            Execution results
        """
        results = []
        for step in workflow.steps:
            result = self._execute_step(step)
            results.append(result)

        return {"success": True, "results": results}

    def _execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step

        Args:
            step: Step definition

        Returns:
            Step result
        """
        return {"success": True, "step": step}
