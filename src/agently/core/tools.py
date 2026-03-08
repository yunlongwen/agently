"""Tool System - Tool registration and execution"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Type
import functools


@dataclass
class ToolResult:
    """Result of tool execution"""
    success: bool
    output: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseTool(ABC):
    """
    Base class for all tools

    Tools are the building blocks for agent actions.
    """

    name: str = ""
    description: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)

    @abstractmethod
    def run(self, **kwargs) -> ToolResult:
        """Execute the tool"""
        pass

    def safe_run(self, **kwargs) -> ToolResult:
        """Execute the tool with error handling"""
        try:
            return self.run(**kwargs)
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def get_schema(self) -> Dict[str, Any]:
        """Get tool schema for LLM"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }

    def to_langchain_tool(self):
        """Convert to LangChain tool format"""
        from langchain_core.tools import StructuredTool

        def wrapper(**kwargs):
            result = self.safe_run(**kwargs)
            if result.success:
                return result.output
            else:
                return f"Error: {result.error}"

        return StructuredTool(
            name=self.name,
            description=self.description,
            func=wrapper,
            args_schema=self.parameters,
        )


class FunctionTool(BaseTool):
    """Tool created from a function"""

    def __init__(
        self,
        func: Callable,
        name: str,
        description: str,
        parameters: Optional[Dict[str, Any]] = None,
    ):
        self.func = func
        self.name = name
        self.description = description
        self.parameters = parameters or {}

    def run(self, *args, **kwargs) -> ToolResult:
        """Execute the function"""
        result = self.func(*args, **kwargs)
        return ToolResult(success=True, output=result)


def tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    parameters: Optional[Dict[str, Any]] = None,
):
    """
    Decorator to create a tool from a function

    Args:
        name: Tool name (defaults to function name)
        description: Tool description
        parameters: Tool parameters schema

    Returns:
        Decorated function as a tool
    """
    def decorator(func: Callable) -> FunctionTool:
        tool_name = name or func.__name__
        tool_description = description or func.__doc__ or f"Tool: {tool_name}"

        return FunctionTool(
            func=func,
            name=tool_name,
            description=tool_description,
            parameters=parameters,
        )

    return decorator


class ToolRegistry:
    """
    Tool Registry - 工具注册表

    管理所有可用工具的注册和查找。
    """

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool"""
        self._tools[tool.name] = tool

    def unregister(self, name: str) -> None:
        """Unregister a tool"""
        if name in self._tools:
            del self._tools[name]

    def get(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name"""
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        """List all registered tool names"""
        return list(self._tools.keys())

    def get_all_schemas(self) -> List[Dict[str, Any]]:
        """Get schemas for all tools"""
        return [tool.get_schema() for tool in self._tools.values()]

    def get_langchain_tools(self) -> List[Any]:
        """Get all tools in LangChain format"""
        return [tool.to_langchain_tool() for tool in self._tools.values()]

    def clear(self) -> None:
        """Clear all registered tools"""
        self._tools.clear()


class ToolExecutor:
    """
    Tool Executor - 工具执行器

    执行工具调用并管理执行上下文。
    """

    def __init__(self, registry: Optional[ToolRegistry] = None):
        self.registry = registry or ToolRegistry()
        self.execution_history: List[Dict[str, Any]] = []

    def execute(self, tool_name: str, **kwargs) -> ToolResult:
        """
        Execute a tool by name

        Args:
            tool_name: Name of the tool to execute
            **kwargs: Tool parameters

        Returns:
            Tool execution result
        """
        tool = self.registry.get(tool_name)

        if tool is None:
            return ToolResult(
                success=False,
                error=f"Tool '{tool_name}' not found",
            )

        result = tool.safe_run(**kwargs)

        # Record execution
        self.execution_history.append({
            "tool": tool_name,
            "parameters": kwargs,
            "success": result.success,
            "output": result.output if result.success else None,
            "error": result.error if not result.success else None,
        })

        return result

    def get_history(self) -> List[Dict[str, Any]]:
        """Get execution history"""
        return self.execution_history.copy()

    def clear_history(self) -> None:
        """Clear execution history"""
        self.execution_history.clear()


# Built-in tools
class ReadFileTool(BaseTool):
    """Tool to read file contents"""

    name = "read_file"
    description = "Read the contents of a file"
    parameters = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file to read",
            }
        },
        "required": ["file_path"],
    }

    def run(self, file_path: str) -> ToolResult:
        """Read file contents"""
        from pathlib import Path

        path = Path(file_path)
        if not path.exists():
            return ToolResult(success=False, error=f"File not found: {file_path}")

        try:
            content = path.read_text()
            return ToolResult(success=True, output=content)
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class WriteFileTool(BaseTool):
    """Tool to write content to a file"""

    name = "write_file"
    description = "Write content to a file"
    parameters = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file to write",
            },
            "content": {
                "type": "string",
                "description": "Content to write",
            },
        },
        "required": ["file_path", "content"],
    }

    def run(self, file_path: str, content: str) -> ToolResult:
        """Write content to file"""
        from pathlib import Path

        path = Path(file_path)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            return ToolResult(success=True, output=f"Successfully wrote to {file_path}")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class ExecuteShellTool(BaseTool):
    """Tool to execute shell commands"""

    name = "execute_shell"
    description = "Execute a shell command"
    parameters = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "Shell command to execute",
            },
        },
        "required": ["command"],
    }

    def run(self, command: str) -> ToolResult:
        """Execute shell command"""
        import subprocess

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60,
            )
            output = result.stdout or result.stderr
            return ToolResult(
                success=result.returncode == 0,
                output=output,
                error=result.stderr if result.returncode != 0 else None,
            )
        except subprocess.TimeoutExpired:
            return ToolResult(success=False, error="Command timed out")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


def get_default_tools() -> List[BaseTool]:
    """Get list of default tools"""
    return [
        ReadFileTool(),
        WriteFileTool(),
        ExecuteShellTool(),
    ]


def create_default_registry() -> ToolRegistry:
    """Create registry with default tools"""
    registry = ToolRegistry()
    for tool in get_default_tools():
        registry.register(tool)
    return registry
