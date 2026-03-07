"""Task Planner - Plans task execution"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ExecutionPlan:
    """Execution plan for a task"""
    tasks: List[Dict[str, Any]]
    status: str = "pending"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def mark_complete(self) -> None:
        """Mark plan as complete"""
        self.status = "completed"

    def mark_failed(self, error: str) -> None:
        """Mark plan as failed"""
        self.status = "failed"
        self.metadata["error"] = error

    def add_task(self, task: Dict[str, Any]) -> None:
        """Add a task to the plan"""
        self.tasks.append(task)


class TaskPlanner:
    """
    Task Planner - 任务规划器

    分析任务、创建执行计划、分解任务步骤。
    """

    def __init__(self):
        self.plan_history: List[ExecutionPlan] = []

    def create_plan(self, task: str) -> ExecutionPlan:
        """
        Create execution plan for a task

        Args:
            task: Task description

        Returns:
            Execution plan
        """
        # Analyze task
        analysis = self._analyze_task(task)

        # Decompose task
        subtasks = self._decompose_task(task, analysis)

        # Create plan
        plan = ExecutionPlan(
            tasks=subtasks,
            metadata={
                "original_task": task,
                "analysis": analysis,
            }
        )

        self.plan_history.append(plan)
        return plan

    def _analyze_task(self, task: str) -> Dict[str, Any]:
        """Analyze task characteristics"""
        task_lower = task.lower()

        # Determine task type
        task_type = self._identify_task_type(task_lower)

        # Assess complexity
        complexity = self._assess_complexity(task)

        # Identify dependencies
        dependencies = self._identify_dependencies(task_lower)

        return {
            "task_type": task_type,
            "complexity": complexity,
            "dependencies": dependencies,
            "estimated_steps": self._estimate_steps(complexity),
        }

    def _identify_task_type(self, task: str) -> str:
        """Identify task type from keywords"""
        type_keywords = {
            "code-generation": ["生成", "generate", "create", "写", "implement", "code"],
            "code-understanding": ["分析", "analyze", "understand", "阅读", "explain"],
            "bug-fixing": ["修复", "fix", "debug", "bug", "error", "解决"],
            "testing": ["测试", "test", "验证", "verify", "check"],
            "code-review": ["审查", "review", "检查", "inspect", "评估"],
            "refactoring": ["重构", "refactor", "优化", "improve", "clean"],
            "git": ["git", "提交", "分支", "commit", "merge", "pull"],
            "documentation": ["文档", "document", "注释", "comment"],
        }

        for task_type, keywords in type_keywords.items():
            if any(kw in task for kw in keywords):
                return task_type

        return "general"

    def _assess_complexity(self, task: str) -> str:
        """Assess task complexity"""
        length = len(task)
        word_count = len(task.split())

        if length < 50 and word_count < 10:
            return "simple"
        elif length < 200 and word_count < 40:
            return "moderate"
        else:
            return "complex"

    def _identify_dependencies(self, task: str) -> List[str]:
        """Identify task dependencies"""
        dependencies = []

        # Check for file references
        if ".py" in task or ".js" in task or ".ts" in task:
            dependencies.append("file-access")

        # Check for code understanding needs
        if any(kw in task for kw in ["分析", "understand", "explain", "review"]):
            dependencies.append("code-understanding")

        # Check for generation needs
        if any(kw in task for kw in ["生成", "generate", "create", "写"]):
            dependencies.append("code-generation")

        return dependencies

    def _estimate_steps(self, complexity: str) -> int:
        """Estimate number of steps based on complexity"""
        estimates = {
            "simple": 1,
            "moderate": 3,
            "complex": 5,
        }
        return estimates.get(complexity, 3)

    def _decompose_task(
        self,
        task: str,
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Decompose task into subtasks"""
        subtasks = []
        task_type = analysis.get("task_type", "general")
        complexity = analysis.get("complexity", "moderate")

        # Always start with understanding
        subtasks.append({
            "step": 1,
            "action": "understand",
            "description": "理解任务需求",
            "agent": "code-understander",
        })

        # Add main execution step
        agent_mapping = {
            "code-generation": "code-generator",
            "code-understanding": "code-understander",
            "bug-fixing": "bug-fixer",
            "testing": "tester",
            "code-review": "code-reviewer",
            "refactoring": "code-generator",
            "git": "git-manager",
            "documentation": "code-generator",
        }

        main_agent = agent_mapping.get(task_type, "code-generator")
        subtasks.append({
            "step": 2,
            "action": "execute",
            "description": f"执行主要任务: {task_type}",
            "agent": main_agent,
        })

        # Add verification for complex tasks
        if complexity in ["moderate", "complex"]:
            subtasks.append({
                "step": 3,
                "action": "verify",
                "description": "验证结果",
                "agent": "code-reviewer",
            })

        # Add testing for code generation
        if task_type == "code-generation" and complexity != "simple":
            subtasks.append({
                "step": len(subtasks) + 1,
                "action": "test",
                "description": "生成和执行测试",
                "agent": "tester",
            })

        return subtasks

    def optimize_plan(self, plan: ExecutionPlan) -> ExecutionPlan:
        """Optimize execution plan"""
        # Identify parallelizable tasks
        # Merge similar tasks
        # Reorder for efficiency
        return plan
