"""Workflow Engine - Executes workflows"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkflowDefinition:
    """Workflow definition"""
    steps: List[Dict[str, Any]]
    name: str = "default_workflow"
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_step(self, step: Dict[str, Any]) -> None:
        """Add a step to the workflow"""
        self.steps.append(step)

    def insert_step(self, index: int, step: Dict[str, Any]) -> None:
        """Insert a step at specific position"""
        self.steps.insert(index, step)

    def remove_step(self, index: int) -> Optional[Dict[str, Any]]:
        """Remove a step at specific position"""
        if 0 <= index < len(self.steps):
            return self.steps.pop(index)
        return None


class WorkflowEngine:
    """
    Workflow Engine - 工作流引擎

    执行预定义的工作流，管理步骤执行和错误处理。
    """

    def __init__(self):
        self.workflows: Dict[str, WorkflowDefinition] = {}
        self.execution_history: List[Dict[str, Any]] = []

    def register_workflow(self, name: str, workflow: WorkflowDefinition) -> None:
        """Register a workflow"""
        self.workflows[name] = workflow

    def execute(
        self,
        workflow: WorkflowDefinition,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a workflow

        Args:
            workflow: Workflow definition
            context: Execution context

        Returns:
            Execution result
        """
        context = context or {}
        results = []

        try:
            for i, step in enumerate(workflow.steps):
                step_result = self._execute_step(step, context, i)
                results.append(step_result)

                # Stop on failure if not continue_on_error
                if not step_result.get("success", True):
                    if not step.get("continue_on_error", False):
                        return {
                            "success": False,
                            "error": step_result.get("error", "Step failed"),
                            "step_index": i,
                            "results": results,
                        }

            return {
                "success": True,
                "results": results,
                "step_count": len(results),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "results": results,
            }

    def _execute_step(
        self,
        step: Dict[str, Any],
        context: Dict[str, Any],
        index: int
    ) -> Dict[str, Any]:
        """Execute a single step"""
        action = step.get("action", "unknown")

        try:
            # Execute based on action type
            if action == "execute":
                return self._execute_action(step, context)
            elif action == "condition":
                return self._execute_condition(step, context)
            elif action == "parallel":
                return self._execute_parallel(step, context)
            else:
                return {
                    "success": True,
                    "action": action,
                    "message": f"Unknown action: {action}",
                }

        except Exception as e:
            return {
                "success": False,
                "action": action,
                "error": str(e),
            }

    def _execute_action(
        self,
        step: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute an action step"""
        # This would integrate with agent execution
        return {
            "success": True,
            "action": step.get("action"),
            "agent": step.get("agent"),
            "context": context,
        }

    def _execute_condition(
        self,
        step: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a condition step"""
        condition = step.get("condition", "")
        # Simple condition evaluation
        result = self._evaluate_condition(condition, context)

        return {
            "success": True,
            "action": "condition",
            "result": result,
        }

    def _execute_parallel(
        self,
        step: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute parallel steps"""
        sub_steps = step.get("steps", [])
        results = []

        for sub_step in sub_steps:
            result = self._execute_step(sub_step, context, 0)
            results.append(result)

        return {
            "success": all(r.get("success", True) for r in results),
            "action": "parallel",
            "results": results,
        }

    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate a condition"""
        # Simple condition evaluation
        # In production, use a proper expression evaluator
        return True

    def create_workflow_from_template(
        self,
        template_name: str,
        params: Dict[str, Any]
    ) -> Optional[WorkflowDefinition]:
        """Create workflow from template"""
        templates = {
            "code_generation": WorkflowDefinition(
                name="code_generation",
                description="Generate code with review",
                steps=[
                    {"action": "execute", "agent": "code-understander", "description": "Understand context"},
                    {"action": "execute", "agent": "code-generator", "description": "Generate code"},
                    {"action": "execute", "agent": "code-reviewer", "description": "Review code"},
                ]
            ),
            "bug_fixing": WorkflowDefinition(
                name="bug_fixing",
                description="Fix bugs with testing",
                steps=[
                    {"action": "execute", "agent": "code-understander", "description": "Understand code"},
                    {"action": "execute", "agent": "bug-fixer", "description": "Fix bug"},
                    {"action": "execute", "agent": "tester", "description": "Verify fix"},
                ]
            ),
        }

        template = templates.get(template_name)
        if template:
            # Customize with params
            template.metadata["params"] = params

        return template
