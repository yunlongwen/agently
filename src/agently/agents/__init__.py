"""Agents Layer - Multi-Agent System"""

from agently.agents.base import AgentContext, AgentResult, BaseAgent
from agently.agents.nexus import NexusAgent
from agently.agents.specialist import (
    ArchitectureDesignerAgent,
    BugFixerAgent,
    CodeGeneratorAgent,
    CodeReviewerAgent,
    CodeUnderstandingAgent,
    DeployConfiguratorAgent,
    GitManagerAgent,
    RequirementsAnalyzerAgent,
    TesterAgent,
)

__all__ = [
    # Base classes
    "BaseAgent",
    "AgentContext",
    "AgentResult",
    # Meta agent
    "NexusAgent",
    # Specialist agents
    "RequirementsAnalyzerAgent",
    "ArchitectureDesignerAgent",
    "CodeGeneratorAgent",
    "CodeUnderstandingAgent",
    "BugFixerAgent",
    "TesterAgent",
    "CodeReviewerAgent",
    "GitManagerAgent",
    "DeployConfiguratorAgent",
]
