# PROJECT KNOWLEDGE BASE

**Generated:** 2026-03-08T01:50:33Z
**Commit:** aa06bf3
**Branch:** master

## OVERVIEW
AI-driven programming assistant for software development lifecycle using multi-agent coordination. Python 3.9+ with Click CLI, LangChain integration, and comprehensive code understanding.

## STRUCTURE
```
agently/
├── src/agently/
│   ├── core/          # LLM, Tools, Skills, CodeUnderstanding
│   ├── orchestrator/   # Nexus, Planner, Scheduler, Workflow, State
│   ├── agents/         # BaseAgent, Specialist agents, NexusAgent
│   ├── infrastructure/  # FileSystem, Git, StateStorage
│   ├── constraints/    # Concurrency, Memory, Security, Timing
│   └── cli/           # Click-based command interface
├── tests/unit/           # Organized by module
├── docs/                # Architecture, user guides
└── config/              # Environment configs
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| CLI entry | `src/agently/cli/main.py` | Click-based, commands: chat/ask/agent/config/task |
| Core services | `src/agently/core/` | LLM, Tools, Skills, CodeUnderstanding |
| Agent coordination | `src/agently/orchestrator/` | Nexus, Planner, Scheduler, Workflow, State |
| Agent implementations | `src/agently/agents/` | BaseAgent, Specialist, NexusAgent |
| Infrastructure | `src/agently/infrastructure/` | File, Git, State services |
| Constraints | `src/agently/constraints/` | Resource management: concurrency/memory/security/timing |
| Config | `src/agently/config.py` | Settings from env/file, integrates constraints |

## CONVENTIONS

**Python:**
- Line length: 100 chars (ruff)
- Type hints required (mypy strict mode)
- Docstrings: Google-style with Args/Returns/Raises
- `__init__.py`: Unused imports allowed (F401)

**Testing:**
- pytest with coverage (terminal + HTML)
- Markers: unit, integration, slow
- Tests in `tests/unit/{module}/`

**Build/CI:**
- Makefile: install, test, lint (ruff), format, type-check (mypy), docs
- GitHub Actions: ci.yml, release.yml, docs.yml
- Package: hatchling

**Logging:**
- Structured logging via structlog
- `agently.logging` module for consistent formatting

## ANTI-PATTERNS (THIS PROJECT)

**Security constraints** (`src/agently/constraints/security.py`):
- Blocked shell patterns: `rm -rf`, `mkfs`, `format`, `dd`, `:(){:|:&};:`

**File operations** (`src/agently/infrastructure/file_system.py`):
- Always validate paths before operations
- Use context managers for file handles

**Concurrency limits** (`src/agently/constraints/concurrency.py`):
- Max 5 concurrent operations by default
- Session cleanup when threshold exceeded

## UNIQUE STYLES

**Multi-agent architecture:**
- Nexus orchestrator coordinates specialist agents
- Capability-based routing (keyword matching)
- AgentContext maintains history across executions

**Tool/Skill system:**
- Registry pattern for dynamic registration
- LangChain integration for external tools
- Skills compose complex workflows from primitives

**Code understanding:**
- AST-based static analysis (504-line service)
- Extracts functions, classes, dependencies
- Call graph generation

## COMMANDS
```bash
make install      # Install dependencies
make test         # Run tests with coverage
make lint         # Ruff linting
make format       # Ruff formatting
make type-check    # MyPy type checking
make build         # Build package
make docs         # Generate docs
```

## NOTES

**Complexity hotspots:**
- `src/agently/core/code_understanding.py` (504 lines) - AST parsing, call graphs
- `src/agently/orchestrator/` - Multi-agent coordination logic

**Stub implementations:**
- CLI commands mostly placeholder ("coming soon!")
- Many specialist agents stubbed (`return {"fixed": True}`)

**Documentation:**
- Chinese descriptions, English code/comments
- Architecture docs in `docs/` with Mermaid diagrams

**Dependencies:**
- Core: Click, Pydantic, LangChain
- Analysis: tree-sitter for parsing
- Git: GitPython
- Storage: aiosqlite (planned, using JSON currently)
