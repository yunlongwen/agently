"""Nexus orchestrator agent"""

from typing import Dict, List, Optional

from agently.agents.base import AgentContext, AgentResult, BaseAgent


class NexusAgent(BaseAgent):
    """Nexus agent - orchestrates multiple specialist agents"""

    def __init__(self):
        super().__init__(
            name="nexus",
            description="综合协调智能体，负责理解和分解任务，调度专业智能体执行",
            capabilities=["orchestration", "task-decomposition", "agent-coordination"],
        )
        self.agents: Dict[str, BaseAgent] = {}

    def register_agent(self, agent: BaseAgent) -> None:
        """Register a specialist agent

        Args:
            agent: Agent to register
        """
        self.agents[agent.name] = agent

    def execute(self, context: AgentContext) -> AgentResult:
        """Execute task by delegating to appropriate specialist

        Args:
            context: Execution context

        Returns:
            Execution result
        """
        selected_agent = self._select_agent(context.task)
        if selected_agent is None:
            return AgentResult(
                success=False,
                error="No suitable agent found for task",
            )

        return selected_agent.execute(context)

    def _select_agent(self, task: str) -> Optional[BaseAgent]:
        """Select appropriate agent for task

        Args:
            task: Task description

        Returns:
            Selected agent or None
        """
        for agent in self.agents.values():
            if self._can_handle(agent, task):
                return agent
        return None

    def _can_handle(self, agent: BaseAgent, task: str) -> bool:
        """Check if agent can handle task

        Args:
            agent: Agent to check
            task: Task description

        Returns:
            True if agent can handle task
        """
        task_lower = task.lower()
        for capability in agent.capabilities:
            if capability in task_lower:
                return True
        return False
