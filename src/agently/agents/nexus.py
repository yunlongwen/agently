"""Nexus - Meta Agent for orchestrating specialist agents"""

from typing import Any, Dict, List, Optional

from agently.agents.base import AgentContext, AgentResult, BaseAgent


class NexusAgent(BaseAgent):
    """
    Nexus - 综合智能体

    作为多智能体系统的中心协调者，负责任务理解、计划生成、
    智能体调度和结果整合。
    """

    def __init__(self):
        super().__init__(
            name="nexus",
            description="Nexus综合智能体 - 协调多个专业智能体完成复杂任务",
            capabilities=[
                "task-planning",
                "agent-orchestration",
                "result-integration",
                "context-management",
            ]
        )
        self.agents: Dict[str, BaseAgent] = {}
        self.execution_history: List[Dict[str, Any]] = []

    def register_agent(self, agent: BaseAgent) -> None:
        """Register a specialist agent"""
        self.agents[agent.name] = agent

    def unregister_agent(self, agent_name: str) -> None:
        """Unregister a specialist agent"""
        if agent_name in self.agents:
            del self.agents[agent_name]

    def execute(self, context: AgentContext) -> AgentResult:
        """
        Execute task using Nexus orchestration

        1. Analyze task and understand requirements
        2. Create execution plan
        3. Select appropriate agents
        4. Execute and coordinate
        5. Integrate results
        """
        try:
            # Step 1: Analyze task
            task_analysis = self._analyze_task(context.task)

            # Step 2: Create execution plan
            plan = self._create_plan(task_analysis)

            # Step 3: Execute plan with agent coordination
            results = self._execute_plan(plan, context)

            # Step 4: Integrate results
            final_result = self._integrate_results(results)

            return AgentResult(
                success=True,
                data=final_result,
                metadata={
                    "plan": plan,
                    "agents_used": list(self.agents.keys()),
                }
            )

        except Exception as e:
            return AgentResult(
                success=False,
                error=str(e),
                metadata={"phase": "execution"}
            )

    def _analyze_task(self, task: str) -> Dict[str, Any]:
        """Analyze task to understand requirements"""
        # Simple keyword-based analysis for now
        task_lower = task.lower()

        analysis = {
            "original_task": task,
            "task_type": self._identify_task_type(task_lower),
            "complexity": self._assess_complexity(task),
            "required_capabilities": self._identify_required_capabilities(task_lower),
        }

        return analysis

    def _identify_task_type(self, task: str) -> str:
        """Identify the type of task"""
        if any(kw in task for kw in ["生成", "generate", "create", "写"]):
            return "code-generation"
        elif any(kw in task for kw in ["分析", "analyze", "understand", "阅读"]):
            return "code-understanding"
        elif any(kw in task for kw in ["修复", "fix", "debug", "bug"]):
            return "bug-fixing"
        elif any(kw in task for kw in ["测试", "test", "验证"]):
            return "testing"
        elif any(kw in task for kw in ["审查", "review", "检查"]):
            return "code-review"
        elif any(kw in task for kw in ["git", "提交", "分支", "commit"]):
            return "git-management"
        else:
            return "general"

    def _assess_complexity(self, task: str) -> str:
        """Assess task complexity"""
        length = len(task)
        if length < 50:
            return "simple"
        elif length < 200:
            return "moderate"
        else:
            return "complex"

    def _identify_required_capabilities(self, task: str) -> List[str]:
        """Identify required capabilities for the task"""
        capabilities = []

        if any(kw in task for kw in ["生成", "generate", "create", "写", "code"]):
            capabilities.append("code-generation")
        if any(kw in task for kw in ["分析", "analyze", "understand", "阅读"]):
            capabilities.append("code-understanding")
        if any(kw in task for kw in ["修复", "fix", "debug", "bug"]):
            capabilities.append("bug-fixing")
        if any(kw in task for kw in ["测试", "test"]):
            capabilities.append("testing")
        if any(kw in task for kw in ["审查", "review"]):
            capabilities.append("code-review")

        return capabilities

    def _create_plan(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create execution plan based on analysis"""
        plan = []

        # Add task understanding step
        plan.append({
            "step": 1,
            "action": "understand",
            "agent": "code-understander",
            "description": "理解任务和代码上下文"
        })

        # Add main execution step based on task type
        task_type = analysis.get("task_type", "general")
        agent_mapping = {
            "code-generation": "code-generator",
            "code-understanding": "code-understander",
            "bug-fixing": "bug-fixer",
            "testing": "tester",
            "code-review": "code-reviewer",
            "git-management": "git-manager",
        }

        main_agent = agent_mapping.get(task_type, "code-generator")
        plan.append({
            "step": 2,
            "action": "execute",
            "agent": main_agent,
            "description": f"执行主要任务: {task_type}"
        })

        # Add verification step for code generation
        if task_type == "code-generation":
            plan.append({
                "step": 3,
                "action": "verify",
                "agent": "code-reviewer",
                "description": "审查生成的代码"
            })

        return plan

    def _execute_plan(
        self,
        plan: List[Dict[str, Any]],
        context: AgentContext
    ) -> List[AgentResult]:
        """Execute the plan with agent coordination"""
        results = []

        for step in plan:
            agent_name = step.get("agent")
            if agent_name and agent_name in self.agents:
                agent = self.agents[agent_name]
                step_context = AgentContext(
                    task=context.task,
                    context={
                        **context.context,
                        "step": step,
                        "previous_results": results,
                    },
                    history=context.history,
                    session_id=context.session_id,
                )
                result = agent.execute(step_context)
                results.append(result)

                # Stop on failure
                if not result.success:
                    break

        return results

    def _integrate_results(self, results: List[AgentResult]) -> Dict[str, Any]:
        """Integrate results from multiple agents"""
        integrated = {
            "success": all(r.success for r in results),
            "results": [],
            "summary": {},
        }

        for i, result in enumerate(results):
            integrated["results"].append({
                "step": i + 1,
                "success": result.success,
                "data": result.data,
                "error": result.error,
            })

        return integrated

    def _select_agent(self, task_type: str) -> Optional[BaseAgent]:
        """Select appropriate agent for task type"""
        agent_mapping = {
            "code-generation": "code-generator",
            "code-understanding": "code-understander",
            "bug-fixing": "bug-fixer",
            "testing": "tester",
            "code-review": "code-reviewer",
            "git-management": "git-manager",
        }

        agent_name = agent_mapping.get(task_type)
        if agent_name and agent_name in self.agents:
            return self.agents[agent_name]

        # Find agent by capability
        for agent in self.agents.values():
            if agent.can_handle(task_type):
                return agent

        return None

    def list_agents(self) -> List[Dict[str, Any]]:
        """List all registered agents"""
        return [agent.get_info() for agent in self.agents.values()]
