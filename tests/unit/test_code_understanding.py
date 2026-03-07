"""Tests for code understanding service"""

from pathlib import Path

import pytest

from agently.core.code_understanding import CodeUnderstandingService


class TestCodeUnderstandingService:
    """Test CodeUnderstandingService class"""

    def test_parse_python_code(self, tmp_path: Path):
        """Test parsing Python code"""
        # Setup
        code_file = tmp_path / "test.py"
        code = """
def hello_world():
    print("Hello, World!")
"""
        code_file.write_text(code)

        # Test
        service = CodeUnderstandingService()
        ast = service.parse_python_code(code_file)

        # Assert
        assert ast is not None
        assert hasattr(ast, "body")
        assert len(ast.body) > 0

    def test_extract_functions(self, tmp_path: Path):
        """Test extracting functions from code"""
        # Setup
        code_file = tmp_path / "test.py"
        code = """
def function_one():
    pass

def function_two(arg1, arg2):
    return arg1 + arg2

class MyClass:
    def method_one(self):
        pass
"""
        code_file.write_text(code)

        # Test
        service = CodeUnderstandingService()
        functions = service.extract_functions(code_file)

        # Assert
        assert len(functions) >= 3  # 2 functions + 1 class method
        function_names = [f.name for f in functions]
        assert "function_one" in function_names
        assert "function_two" in function_names
        assert "method_one" in function_names

    def test_extract_classes(self, tmp_path: Path):
        """Test extracting classes from code"""
        # Setup
        code_file = tmp_path / "test.py"
        code = """
class ClassOne:
    pass

class ClassTwo:
    pass
"""
        code_file.write_text(code)

        # Test
        service = CodeUnderstandingService()
        classes = service.extract_classes(code_file)

        # Assert
        assert len(classes) == 2
        class_names = [c.name for c in classes]
        assert "ClassOne" in class_names
        assert "ClassTwo" in class_names

    def test_get_file_structure(self, tmp_path: Path):
        """Test getting file structure"""
        # Setup
        code_file = tmp_path / "test.py"
        code = """
class MyClass:
    def method_one(self):
        pass

def function_one():
    pass
"""
        code_file.write_text(code)

        # Test
        service = CodeUnderstandingService()
        structure = service.get_file_structure(code_file)

        # Assert
        assert "classes" in structure
        assert "functions" in structure
        assert len(structure["classes"]) >= 1
        assert len(structure["functions"]) >= 1
