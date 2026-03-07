"""Nexus Orchestrator - Main orchestration logic"""

from typing import Any, Dict, List, Optional

from agently.agents.base import AgentContext, AgentResult, BaseAgent
from agently.agents.nexus import NexusAgent
from agently.orchestrator.planner import ExecutionPlan, TaskPlanner
from agently.orchestrator.scheduler import AgentScheduler
from agently.orchestrator.state import StateManager
from agently.orchestrator.workflow import WorkflowDefinition, WorkflowEngine


class NexusOrchestrator:
    """
    Nexus Orchestrator - 智能体协调器

    协调Nexus综合智能体和专业智能体，负责任务规划、调度、状态管理和工作流执行。
    """

    def __init__(self):
        self.nexus = NexusAgent()
        self.planner = TaskPlanner()
        self.scheduler = AgentScheduler()
        self.state_manager = StateManager()
        self.workflow_engine = WorkflowEngine()
        self._setup_agents()

    def _setup_agents(self) -> None:
        """Setup and register all specialist agents"""
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

        agents = [
            RequirementsAnalyzerAgent(),
            ArchitectureDesignerAgent(),
            CodeGeneratorAgent(),
            CodeUnderstandingAgent(),
            BugFixerAgent(),
            TesterAgent(),
            CodeReviewerAgent(),
            GitManagerAgent(),
            DeployConfiguratorAgent(),
        ]

        for agent in agents:
            self.nexus.register_agent(agent)
            self.scheduler.register_agent(agent)

    def process_task(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a task through the orchestration pipeline

        Args:
            task: The task description
            context: Additional context
            session_id: Session identifier

        Returns:
            Execution result
        """
        try:
            # Create agent context
            agent_context = AgentContext(
                task=task,
                context=context or {},
                session_id=session_id,
            )

            # Step 1: Create execution plan
            plan = self.planner.create_plan(task)

            # Step 2: Execute through Nexus
            result = self.nexus.execute(agent_context)

            # Step 3: Update state
            if session_id:
                self.state_manager.update_state(
                    session_id,
                    {
                        "last_task": task,
                        "last_result": result.data if result.success else None,
                        "last_error": result.error if not result.success else None,
                    }
                )

            return {
                "success": result.success,
                "data": result.data,
                "error": result.error,
                "metadata": result.metadata,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": {},
            }

    def execute_workflow(
        self,
        workflow: WorkflowDefinition,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a predefined workflow"""
        return self.workflow_engine.execute(workflow, context or {})

    def get_available_agents(self) -> List[Dict[str, Any]]:
        """Get list of available agents"""
        return self.nexus.list_agents()

    def get_session_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get state for a session"""
        return self.state_manager.get_state(session_id)
