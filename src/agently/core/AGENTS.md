# CORE SERVICES LAYER

## OVERVIEW
Provides core capabilities: LLM integration, tool execution, skill composition, and AST-based code understanding.

## STRUCTURE
```
core/
├── llm_service.py         # Chat, streaming, embeddings, token counting
├── tools.py               # Tool registry, executors, built-in tools
├── skills.py              # Skill system for complex workflows
├── code_understanding.py   # AST-based code analysis (504 lines)
└── model_service.py       # Legacy model integration
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| LLM chat/streaming | `llm_service.py` | OpenAI, Anthropic support |
| Tool registration | `tools.py:ToolRegistry` | Dynamic tool management |
| Built-in tools | `tools.py` | FileTool, ShellTool with security checks |
| Skill composition | `skills.py` | Multi-step workflow definition |
| Code analysis | `code_understanding.py` | AST parsing, functions/classes, dependencies |

## CONVENTIONS

**Tool/Skill pattern:**
- Registry-based: `ToolRegistry.register()`, `SkillRegistry.register()`
- Result objects: `ToolResult(success, data, error)`, `SkillResult(success, output, steps)`
- Built-in tools inherit from `BaseTool`

**LLM service:**
- `LLMConfig` for provider/model params
- Streaming via async generators
- Token counting and cost tracking

**Code understanding:**
- Dataclasses for parsed entities: `FunctionInfo`, `ClassInfo`, `ImportInfo`
- `ast` module for static analysis
- Complexity metrics (cyclomatic complexity)

## ANTI-PATTERNS (THIS LAYER)

**Tool execution:**
- Always validate via `SecurityManager` before shell commands
- Return `ToolResult` with consistent structure

**Code understanding:**
- Use tree-sitter for language-agnostic parsing (future)
- Current: Python `ast` module only

## UNIQUE STYLES

**Registry pattern:** Tools/skills register at module import time for lazy loading

**Built-in tools:** File operations and shell commands with security validation via constraints module

**Code analysis:** Deep AST integration - extracts functions, classes, docstrings, call graphs, dependencies

## NOTES

**Complexity hotspot:** `code_understanding.py` is the largest single file (504 lines) - consider splitting if it grows further

**Legacy:** `model_service.py` marked as legacy - prefer `llm_service.py` for new code

**Integration:** Tools integrate with LangChain for external tool compatibility
