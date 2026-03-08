"""Tests for tool system"""

import pytest
from unittest.mock import Mock, patch

from agently.core.tools import (
    BaseTool,
    ToolRegistry,
    ToolExecutor,
    ToolResult,
    tool,
)


class TestToolResult:
    """Test ToolResult"""

    def test_success_result(self):
        """Test successful tool result"""
        result = ToolResult(success=True, output="Done")
        assert result.success is True
        assert result.output == "Done"
        assert result.error is None

    def test_error_result(self):
        """Test error tool result"""
        result = ToolResult(success=False, error="Something went wrong")
        assert result.success is False
        assert result.error == "Something went wrong"


class TestBaseTool:
    """Test BaseTool"""

    def test_tool_creation(self):
        """Test creating a tool"""
        class EchoTool(BaseTool):
            name = "echo"
            description = "Echo the input"

            def run(self, text: str) -> ToolResult:
                return ToolResult(success=True, output=text)

        tool = EchoTool()
        assert tool.name == "echo"
        assert tool.description == "Echo the input"

    def test_tool_execution(self):
        """Test executing a tool"""
        class EchoTool(BaseTool):
            name = "echo"
            description = "Echo the input"

            def run(self, text: str) -> ToolResult:
                return ToolResult(success=True, output=text)

        tool = EchoTool()
        result = tool.run("hello")
        assert result.success is True
        assert result.output == "hello"

    def test_tool_with_error(self):
        """Test tool that raises error"""
        class ErrorTool(BaseTool):
            name = "error_tool"
            description = "Always errors"

            def run(self) -> ToolResult:
                raise ValueError("Test error")

        tool = ErrorTool()
        result = tool.safe_run()
        assert result.success is False
        assert "error" in result.error.lower()


class TestToolDecorator:
    """Test @tool decorator"""

    def test_decorator_creates_tool(self):
        """Test that decorator creates a tool"""
        @tool(name="add", description="Add two numbers")
        def add_numbers(a: int, b: int) -> int:
            return a + b

        assert add_numbers.name == "add"
        assert add_numbers.description == "Add two numbers"

    def test_decorated_tool_execution(self):
        """Test executing decorated tool"""
        @tool(name="multiply", description="Multiply two numbers")
        def multiply(a: int, b: int) -> int:
            return a * b

        result = multiply.run(3, 4)
        assert result.success is True
        assert result.output == 12


class TestToolRegistry:
    """Test ToolRegistry"""

    def test_register_tool(self):
        """Test registering a tool"""
        registry = ToolRegistry()

        class TestTool(BaseTool):
            name = "test"
            description = "Test tool"
            def run(self) -> ToolResult:
                return ToolResult(success=True, output="test")

        registry.register(TestTool())
        assert "test" in registry.list_tools()

    def test_get_tool(self):
        """Test getting a tool by name"""
        registry = ToolRegistry()

        class EchoTool(BaseTool):
            name = "echo"
            description = "Echo tool"
            def run(self, text: str) -> ToolResult:
                return ToolResult(success=True, output=text)

        tool = EchoTool()
        registry.register(tool)

        retrieved = registry.get("echo")
        assert retrieved is not None
        assert retrieved.name == "echo"

    def test_get_nonexistent_tool(self):
        """Test getting a tool that doesn't exist"""
        registry = ToolRegistry()
        tool = registry.get("nonexistent")
        assert tool is None

    def test_list_tools(self):
        """Test listing all tools"""
        registry = ToolRegistry()

        class Tool1(BaseTool):
            name = "tool1"
            description = "Tool 1"
            def run(self) -> ToolResult:
                return ToolResult(success=True)

        class Tool2(BaseTool):
            name = "tool2"
            description = "Tool 2"
            def run(self) -> ToolResult:
                return ToolResult(success=True)

        registry.register(Tool1())
        registry.register(Tool2())

        tools = registry.list_tools()
        assert "tool1" in tools
        assert "tool2" in tools

    def test_unregister_tool(self):
        """Test unregistering a tool"""
        registry = ToolRegistry()

        class TestTool(BaseTool):
            name = "test"
            description = "Test"
            def run(self) -> ToolResult:
                return ToolResult(success=True)

        registry.register(TestTool())
        assert "test" in registry.list_tools()

        registry.unregister("test")
        assert "test" not in registry.list_tools()


class TestToolExecutor:
    """Test ToolExecutor"""

    def test_execute_tool(self):
        """Test executing a tool through executor"""
        registry = ToolRegistry()

        class EchoTool(BaseTool):
            name = "echo"
            description = "Echo tool"
            def run(self, text: str) -> ToolResult:
                return ToolResult(success=True, output=text)

        registry.register(EchoTool())
        executor = ToolExecutor(registry)

        result = executor.execute("echo", text="hello")
        assert result.success is True
        assert result.output == "hello"

    def test_execute_nonexistent_tool(self):
        """Test executing a tool that doesn't exist"""
        registry = ToolRegistry()
        executor = ToolExecutor(registry)

        result = executor.execute("nonexistent")
        assert result.success is False
        assert "not found" in result.error.lower()

    def test_execute_with_validation(self):
        """Test executing with parameter validation"""
        registry = ToolRegistry()

        class AddTool(BaseTool):
            name = "add"
            description = "Add numbers"
            def run(self, a: int, b: int) -> ToolResult:
                return ToolResult(success=True, output=a + b)

        registry.register(AddTool())
        executor = ToolExecutor(registry)

        result = executor.execute("add", a=1, b=2)
        assert result.success is True
        assert result.output == 3
