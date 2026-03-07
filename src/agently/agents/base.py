"""Base agent classes and interfaces"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentContext:
    """Context for agent execution"""
    task: str
    context: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)
    session_id: Optional[str] = None


@dataclass
class AgentResult:
    """Result from agent execution"""
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Base class for all agents"""

    def __init__(
        self,
        name: str,
        description: str,
        capabilities: Optional[List[str]] = None
    ):
        self.name = name
        self.description = description
        self.capabilities = capabilities or []

    @abstractmethod
    def execute(self, context: AgentContext) -> AgentResult:
        """Execute the agent with given context"""
        pass

    def can_handle(self, task_type: str) -> bool:
        """Check if agent can handle given task type"""
        return task_type in self.capabilities

    def get_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities,
        }
