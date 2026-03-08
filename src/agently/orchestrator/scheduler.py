"""Agent scheduler for orchestrator"""

from typing import Any, Optional

from agently.agents.base import BaseAgent


class AgentScheduler:
    """Schedules and manages agents"""

    def __init__(self):
        self.agents: dict[str, BaseAgent] = {}

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent

        Args:
            agent: Agent to register
        """
        self.agents[agent.name] = agent

    def schedule_agent(self, capability: str, context: dict[str, Any]) -> Optional[BaseAgent]:
        """Schedule appropriate agent for capability

        Args:
            capability: Required capability
            context: Execution context

        Returns:
            Selected agent or None
        """
        for agent in self.agents.values():
            if self._can_handle(agent, capability):
                return agent
        return None

    def _can_handle(self, agent: BaseAgent, capability: str) -> bool:
        """Check if agent can handle capability

        Args:
            agent: Agent to check
            capability: Required capability

        Returns:
            True if agent can handle
        """
        capabilities = getattr(agent, "capabilities", [])
        return capability in capabilities
