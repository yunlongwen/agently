# ORCHESTRATOR LAYER

## OVERVIEW
Coordinates multi-agent workflows: task decomposition, agent scheduling, state management, workflow execution.

## STRUCTURE
```
orchestrator/
├── nexus.py        # Main coordinator integrating all components
├── planner.py      # TaskPlanner: task breakdown, ExecutionPlan
├── scheduler.py     # AgentScheduler: capability-based agent selection
├── workflow.py     # WorkflowEngine: multi-step execution, WorkflowDefinition
└── state.py        # StateManager: global/session state management
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Main coordinator | `nexus.py:NexusOrchestrator` | Integrates planner/scheduler/state/workflow |
| Task planning | `planner.py:TaskPlanner` | Breaks down high-level tasks into steps |
| Agent selection | `scheduler.py:AgentScheduler` | Capability matching against tasks |
| Workflow execution | `workflow.py:WorkflowEngine` | Executes multi-step workflows |
| State management | `state.py:StateManager` | Maintains context across agents |

## CONVENTIONS

**Planning:**
- `TaskPlanner.plan_task()` → `ExecutionPlan` with sequential steps
- Each step has: description, agent_type, parameters

**Scheduling:**
- `AgentScheduler.select_agent(task)` based on capability keywords
- Agents register capabilities as string arrays

**Workflow:**
- `WorkflowDefinition` uses dataclasses for step definitions
- Supports extensible step patterns

**State:**
- `StateManager` maintains global and session state
- Context shared between agent executions

## ANTI-PATTERNS (THIS LAYER)

**Agent selection:**
- Simple keyword matching - may need refinement as agents grow
- Avoid hard-coded agent names - use capability-based routing

**State management:**
- Race conditions possible with concurrent agents
- Use locks for shared state access

## UNIQUE STYLES

**Hybrid coordinator:** `NexusOrchestrator` integrates planner/scheduler/workflow/state via dependency injection

**Capability routing:** Agents selected by matching task requirements against agent capabilities

**Step-by-step execution:** Complex tasks decomposed into sequential steps managed by workflow engine

**Cross-agent context:** StateManager enables context sharing between agent interactions

## NOTES

**NexusAgent integration:** `src/agently/agents/nexus.py` uses orchestrator to delegate to specialist agents

**Integration:** Orchestrator components used by `agents/nexus.py:NexusAgent` for task delegation

**Testing:** Comprehensive unit tests in `tests/unit/orchestrator/test_orchestrator.py`

**Complexity hotspots:**
- Agent selection logic (`scheduler.py`) - O(n) matching, optimize for many agents
- State coordination between multiple agents - ensure thread safety
- Multi-step workflow failure recovery - needs robust error handling
