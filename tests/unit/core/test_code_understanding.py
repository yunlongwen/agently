"""Tests for enhanced code understanding"""

import ast
from pathlib import Path
import pytest
from unittest.mock import Mock, patch

from agently.core.code_understanding import (
    CodeUnderstandingService,
    CodeStructure,
    FunctionInfo,
    ClassInfo,
    ImportInfo,
)


class TestFunctionInfo:
    """Test FunctionInfo"""

    def test_function_info_creation(self):
        """Test creating function info"""
        info = FunctionInfo(
            name="test_func",
            args=["a", "b"],
            returns="str",
            docstring="Test function",
            line_start=1,
            line_end=5,
        )
        assert info.name == "test_func"
        assert info.args == ["a", "b"]
        assert info.returns == "str"


class TestClassInfo:
    """Test ClassInfo"""

    def test_class_info_creation(self):
        """Test creating class info"""
        info = ClassInfo(
            name="TestClass",
            bases=["BaseClass"],
            methods=["__init__", "run"],
            docstring="Test class",
            line_start=1,
            line_end=20,
        )
        assert info.name == "TestClass"
        assert info.bases == ["BaseClass"]
        assert len(info.methods) == 2


class TestImportInfo:
    """Test ImportInfo"""

    def test_import_info_creation(self):
        """Test creating import info"""
        info = ImportInfo(
            module="os.path",
            names=["join", "dirname"],
            alias="osp",
            is_from=True,
        )
        assert info.module == "os.path"
        assert info.names == ["join", "dirname"]
        assert info.is_from is True


class TestCodeStructure:
    """Test CodeStructure"""

    def test_code_structure_creation(self):
        """Test creating code structure"""
        structure = CodeStructure(
            file_path="/test/file.py",
            imports=[],
            classes=[],
            functions=[],
            variables=[],
        )
        assert structure.file_path == "/test/file.py"


class TestCodeUnderstandingService:
    """Test CodeUnderstandingService"""

    @pytest.fixture
    def service(self):
        """Create service instance"""
        return CodeUnderstandingService()

    @pytest.fixture
    def sample_code(self, tmp_path: Path) -> Path:
        """Create sample Python file"""
        code = '''
"""Module docstring"""

import os
from typing import List, Optional

class Calculator:
    """A simple calculator"""
    
    def __init__(self, name: str):
        self.name = name
    
    def add(self, a: int, b: int) -> int:
        """Add two numbers"""
        return a + b
    
    def multiply(self, a: int, b: int) -> int:
        """Multiply two numbers"""
        return a * b

def calculate_sum(numbers: List[int]) -> int:
    """Calculate sum of numbers"""
    return sum(numbers)

CONSTANT = 42
'''
        file_path = tmp_path / "sample.py"
        file_path.write_text(code)
        return file_path

    def test_parse_python_code(self, service: CodeUnderstandingService, sample_code: Path):
        """Test parsing Python code"""
        tree = service.parse_python_code(sample_code)
        assert isinstance(tree, ast.AST)

    def test_extract_functions(self, service: CodeUnderstandingService, sample_code: Path):
        """Test extracting functions"""
        functions = service.extract_functions(sample_code)
        # Should find: __init__, add, multiply, calculate_sum
        assert len(functions) >= 3

    def test_extract_classes(self, service: CodeUnderstandingService, sample_code: Path):
        """Test extracting classes"""
        classes = service.extract_classes(sample_code)
        assert len(classes) >= 1
        assert any(c.name == "Calculator" for c in classes)

    def test_get_file_structure(self, service: CodeUnderstandingService, sample_code: Path):
        """Test getting file structure"""
        structure = service.get_file_structure(sample_code)
        assert "classes" in structure
        assert "functions" in structure
        assert "imports" in structure
        assert "Calculator" in structure["classes"]

    def test_get_detailed_structure(self, service: CodeUnderstandingService, sample_code: Path):
        """Test getting detailed structure"""
        structure = service.get_detailed_structure(sample_code)
        assert structure is not None
        assert len(structure.classes) >= 1
        assert len(structure.functions) >= 1

    def test_find_symbol_definition(self, service: CodeUnderstandingService, sample_code: Path):
        """Test finding symbol definition"""
        result = service.find_symbol_definition(sample_code, "Calculator")
        assert result is not None
        assert result["name"] == "Calculator"
        assert result["type"] == "class"

    def test_find_symbol_definition_function(self, service: CodeUnderstandingService, sample_code: Path):
        """Test finding function definition"""
        result = service.find_symbol_definition(sample_code, "calculate_sum")
        assert result is not None
        assert result["type"] == "function"

    def test_find_symbol_not_found(self, service: CodeUnderstandingService, sample_code: Path):
        """Test finding non-existent symbol"""
        result = service.find_symbol_definition(sample_code, "nonexistent")
        assert result is None

    def test_get_imports(self, service: CodeUnderstandingService, sample_code: Path):
        """Test getting imports"""
        imports = service.get_imports(sample_code)
        assert len(imports) >= 2
        assert any(imp.module == "os" for imp in imports)

    def test_analyze_dependencies(self, service: CodeUnderstandingService, sample_code: Path):
        """Test analyzing dependencies"""
        deps = service.analyze_dependencies(sample_code)
        assert "os" in deps or "typing" in deps

    def test_get_function_complexity(self, service: CodeUnderstandingService, sample_code: Path):
        """Test getting function complexity"""
        complexity = service.get_function_complexity(sample_code, "add")
        assert complexity >= 1

    def test_extract_docstrings(self, service: CodeUnderstandingService, sample_code: Path):
        """Test extracting docstrings"""
        docstrings = service.extract_docstrings(sample_code)
        assert len(docstrings) >= 1
        assert any("Calculator" in ds or "calculator" in ds.lower() for ds in docstrings)

    def test_parse_invalid_code(self, service: CodeUnderstandingService, tmp_path: Path):
        """Test parsing invalid Python code"""
        invalid_file = tmp_path / "invalid.py"
        invalid_file.write_text("def broken(:\n    pass")
        
        with pytest.raises(SyntaxError):
            service.parse_python_code(invalid_file)

    def test_get_call_graph(self, service: CodeUnderstandingService, sample_code: Path):
        """Test getting call graph"""
        graph = service.get_call_graph(sample_code)
        assert graph is not None
        assert isinstance(graph, dict)

    def test_find_usages(self, service: CodeUnderstandingService, sample_code: Path):
        """Test finding symbol usages"""
        usages = service.find_usages(sample_code, "self.name")
        assert isinstance(usages, list)
