"""Base agent classes and interfaces"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class AgentContext:
    """Context for agent execution"""

    task: str
    context: dict[str, Any] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AgentResult:
    """Result from agent execution"""

    success: bool
    data: dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


class BaseAgent:
    """Base class for all agents"""

    def __init__(
        self,
        name: str,
        description: str,
        capabilities: Optional[list[str]] = None,
    ):
        self.name = name
        self.description = description
        self.capabilities = capabilities or []

    def execute(self, context: AgentContext) -> AgentResult:
        """Execute the agent's task

        Args:
            context: Execution context

        Returns:
            Agent execution result
        """
        raise NotImplementedError("Subclasses must implement execute()")
