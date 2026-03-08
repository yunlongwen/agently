"""Tests for orchestrator layer"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from agently.agents.base import AgentResult
from agently.orchestrator.nexus import NexusOrchestrator
from agently.orchestrator.planner import TaskPlanner, ExecutionPlan
from agently.orchestrator.scheduler import AgentScheduler
from agently.orchestrator.state import StateManager
from agently.orchestrator.workflow import WorkflowEngine, WorkflowDefinition


class TestNexusOrchestrator:
    """Test NexusOrchestrator class"""

    def test_orchestrator_init(self):
        """Test initializing orchestrator"""
        orch = NexusOrchestrator()
        assert orch.planner is not None
        assert orch.scheduler is not None
        assert orch.state_manager is not None
        assert orch.workflow_engine is not None

    def test_orchestrator_process_task(self):
        """Test processing a task through orchestrator"""
        orch = NexusOrchestrator()

        with patch.object(orch.nexus, 'execute') as mock_exec:
            mock_exec.return_value = AgentResult(success=True, data={"result": "done"})

            result = orch.process_task("test task")

        assert result["success"] is True


class TestTaskPlanner:
    """Test TaskPlanner class"""

    def test_planner_init(self):
        """Test initializing task planner"""
        planner = TaskPlanner()
        assert planner is not None

    def test_create_plan(self):
        """Test creating execution plan"""
        planner = TaskPlanner()

        with patch.object(planner, '_analyze_task') as mock_analyze:
            with patch.object(planner, '_decompose_task') as mock_decompose:
                mock_analyze.return_value = {"complexity": "low", "type": "code"}
                mock_decompose.return_value = [{"step": 1, "agent": "code-generator"}]

                plan = planner.create_plan("generate a function")

        assert isinstance(plan, ExecutionPlan)
        assert len(plan.tasks) == 1

    def test_analyze_task_complexity(self):
        """Test analyzing task complexity"""
        planner = TaskPlanner()

        result = planner._analyze_task("simple task")
        assert "complexity" in result


class TestExecutionPlan:
    """Test ExecutionPlan class"""

    def test_plan_init(self):
        """Test initializing execution plan"""
        plan = ExecutionPlan(tasks=[{"step": 1}])
        assert len(plan.tasks) == 1
        assert plan.status == "pending"

    def test_plan_mark_complete(self):
        """Test marking plan as complete"""
        plan = ExecutionPlan(tasks=[])
        plan.mark_complete()
        assert plan.status == "completed"


class TestAgentScheduler:
    """Test AgentScheduler class"""

    def test_scheduler_init(self):
        """Test initializing scheduler"""
        scheduler = AgentScheduler()
        assert scheduler is not None

    def test_schedule_agent(self):
        """Test scheduling an agent"""
        scheduler = AgentScheduler()
        mock_agent = Mock()
        mock_agent.name = "test-agent"
        mock_agent.capabilities = ["code-generation"]

        scheduler.register_agent(mock_agent)
        agent = scheduler.schedule_agent("code-generation", {})

        assert agent.name == "test-agent"


class TestStateManager:
    """Test StateManager class"""

    def test_state_manager_init(self):
        """Test initializing state manager"""
        sm = StateManager()
        assert sm.global_state == {}

    def test_set_and_get_state(self):
        """Test setting and getting state"""
        sm = StateManager()
        sm.set_state("key", "value")
        assert sm.get_state("key") == "value"

    def test_update_state(self):
        """Test updating state"""
        sm = StateManager()
        sm.set_state("context", {"a": 1})
        sm.update_state("context", {"b": 2})
        assert sm.get_state("context") == {"a": 1, "b": 2}


class TestWorkflowEngine:
    """Test WorkflowEngine class"""

    def test_workflow_engine_init(self):
        """Test initializing workflow engine"""
        engine = WorkflowEngine()
        assert engine is not None

    def test_execute_workflow(self):
        """Test executing a workflow"""
        engine = WorkflowEngine()
        workflow = WorkflowDefinition(steps=[{"action": "test"}])

        with patch.object(engine, '_execute_step') as mock_step:
            mock_step.return_value = {"success": True}
            result = engine.execute(workflow)

        assert result["success"] is True


class TestWorkflowDefinition:
    """Test WorkflowDefinition class"""

    def test_workflow_init(self):
        """Test initializing workflow definition"""
        workflow = WorkflowDefinition(steps=[{"action": "step1"}])
        assert len(workflow.steps) == 1
        assert workflow.name is not None

    def test_workflow_add_step(self):
        """Test adding step to workflow"""
        workflow = WorkflowDefinition(steps=[])
        workflow.add_step({"action": "new_step"})
        assert len(workflow.steps) == 1
