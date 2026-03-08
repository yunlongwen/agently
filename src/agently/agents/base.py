"""Base agent classes and interfaces"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentContext:
    """Context for agent execution"""
    task: str
    context: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AgentResult:
    """Result from agent execution"""
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


class BaseAgent:
    """Base class for all agents"""

    def __init__(
        self,
        name: str,
        description: str,
        capabilities: Optional[List[str]] = None,
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
