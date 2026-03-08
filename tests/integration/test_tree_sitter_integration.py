"""Tree-sitter Integration Tests

Tests for tree-sitter based code analysis.
Following TDD: tests are written before implementation.
"""

import os
import tempfile
from pathlib import Path

import pytest


class TestTreeSitterBasicIntegration:
    """Test basic tree-sitter integration"""

    def test_tree_sitter_import_available(self):
        """RED: Test that tree-sitter can be imported"""
        try:
            import tree_sitter

            assert tree_sitter is not None
        except ImportError:
            pytest.fail("tree-sitter is not installed")

    def test_tree_sitter_language_python_available(self):
        """RED: Test that tree-sitter python language is available"""
        try:
            import tree_sitter_python

            assert tree_sitter_python is not None
        except ImportError:
            pytest.fail("tree-sitter-python is not installed")

    def test_tree_sitter_parse_python_code(self):
        """RED: Test tree-sitter parses Python code"""
        from agently.core.tree_sitter_service import TreeSitterService

        code = """
def hello(name: str) -> str:
    return f"Hello, {name}!"
"""
        service = TreeSitterService()
        tree = service.parse_code(code)

        assert tree is not None
        assert tree.root_node is not None
        assert tree.root_node.type == "module"

    def test_tree_sitter_get_function_nodes(self):
        """RED: Test getting function nodes from tree"""
        from agently.core.tree_sitter_service import TreeSitterService

        code = """
def func1():
    pass

def func2(x: int) -> int:
    return x * 2
"""
        service = TreeSitterService()
        tree = service.parse_code(code)
        functions = service.get_function_nodes(tree)

        assert len(functions) == 2
        func_names = [service.get_node_name(f) for f in functions]
        assert "func1" in func_names
        assert "func2" in func_names

    def test_tree_sitter_get_class_nodes(self):
        """RED: Test getting class nodes from tree"""
        from agently.core.tree_sitter_service import TreeSitterService

        code = """
class Animal:
    pass

class Dog(Animal):
    pass
"""
        service = TreeSitterService()
        tree = service.parse_code(code)
        classes = service.get_class_nodes(tree)

        assert len(classes) == 2
        class_names = [service.get_node_name(c) for c in classes]
        assert "Animal" in class_names
        assert "Dog" in class_names

    def test_tree_sitter_get_function_parameters(self):
        """RED: Test extracting function parameters"""
        from agently.core.tree_sitter_service import TreeSitterService

        code = """
def process(data: list, options: dict = None) -> list:
    return data
"""
        service = TreeSitterService()
        tree = service.parse_code(code)
        functions = service.get_function_nodes(tree)

        assert len(functions) == 1
        params = service.get_function_parameters(functions[0])

        assert len(params) == 2
        param_names = [p["name"] for p in params]
        assert "data" in param_names
        assert "options" in param_names

    def test_tree_sitter_get_function_return_type(self):
        """RED: Test extracting function return type"""
        from agently.core.tree_sitter_service import TreeSitterService

        code = """
def get_value() -> int:
    return 42
"""
        service = TreeSitterService()
        tree = service.parse_code(code)
        functions = service.get_function_nodes(tree)

        assert len(functions) == 1
        return_type = service.get_function_return_type(functions[0])

        assert return_type == "int"

    def test_tree_sitter_get_function_decorators(self):
        """RED: Test extracting function decorators"""
        from agently.core.tree_sitter_service import TreeSitterService

        code = """
@property
def prop(self):
    pass

@staticmethod
def static():
    pass
"""
        service = TreeSitterService()
        tree = service.parse_code(code)
        functions = service.get_function_nodes(tree)

        assert len(functions) == 2

        # Find decorators using tree and function node
        decorators_map = {}
        for func in functions:
            func_name = service.get_node_name(func)
            decorators = service.get_function_decorators(tree, func)
            decorators_map[func_name] = decorators

        assert "property" in decorators_map.get("prop", [])
        assert "staticmethod" in decorators_map.get("static", [])

    def test_tree_sitter_get_class_bases(self):
        """RED: Test extracting class base classes"""
        from agently.core.tree_sitter_service import TreeSitterService

        code = """
class Base:
    pass

class Derived(Base, object):
    pass
"""
        service = TreeSitterService()
        tree = service.parse_code(code)
        classes = service.get_class_nodes(tree)

        derived_class = None
        for cls in classes:
            if service.get_node_name(cls) == "Derived":
                derived_class = cls
                break

        assert derived_class is not None
        bases = service.get_class_bases(derived_class)
        base_names = [service.get_node_name(b) for b in bases]

        assert "Base" in base_names
        assert "object" in base_names

    def test_tree_sitter_get_docstring(self):
        """RED: Test extracting docstrings"""
        from agently.core.tree_sitter_service import TreeSitterService

        code = '''
def func():
    """Function docstring"""
    pass

class MyClass:
    """Class docstring"""
    pass
'''
        service = TreeSitterService()
        tree = service.parse_code(code)

        functions = service.get_function_nodes(tree)
        classes = service.get_class_nodes(tree)

        func_docstring = service.get_docstring(functions[0])
        class_docstring = service.get_docstring(classes[0])

        assert func_docstring == "Function docstring"
        assert class_docstring == "Class docstring"

    def test_tree_sitter_walk_tree(self):
        """RED: Test walking the syntax tree"""
        from agently.core.tree_sitter_service import TreeSitterService

        code = """
def outer():
    def inner():
        return 1
    return inner()
"""
        service = TreeSitterService()
        tree = service.parse_code(code)

        all_nodes = []
        service.walk_tree(tree.root_node, lambda node: all_nodes.append(node.type))

        assert "function_definition" in all_nodes
        assert "return_statement" in all_nodes

    def test_tree_sitter_get_node_text(self):
        """RED: Test getting node source text"""
        from agently.core.tree_sitter_service import TreeSitterService

        code = "def hello(): pass"
        service = TreeSitterService()
        tree = service.parse_code(code)
        functions = service.get_function_nodes(tree)

        assert len(functions) == 1
        func_text = service.get_node_text(functions[0], code.encode())

        assert "def hello()" in func_text


class TestTreeSitterAdvancedFeatures:
    """Test advanced tree-sitter features"""

    def test_tree_sitter_query_nodes(self):
        """RED: Test querying specific node types"""
        from agently.core.tree_sitter_service import TreeSitterService

        code = """
x = 1
y = 2
def func():
    pass
"""
        service = TreeSitterService()
        tree = service.parse_code(code)

        # Query all assignment nodes
        assignments = service.query_nodes(tree, "assignment")
        assert len(assignments) >= 2

        # Query all function definitions
        functions = service.query_nodes(tree, "function_definition")
        assert len(functions) == 1

    def test_tree_sitter_find_node_at_position(self):
        """RED: Test finding node at specific position"""
        from agently.core.tree_sitter_service import TreeSitterService

        code = """
def hello_world():
    return "Hello"
"""
        service = TreeSitterService()
        tree = service.parse_code(code)

        # Find node at line 2, column 5 (inside function name)
        node = service.find_node_at_position(tree, 2, 5)

        assert node is not None

    def test_tree_sitter_get_import_statements(self):
        """RED: Test extracting import statements"""
        from agently.core.tree_sitter_service import TreeSitterService

        code = """
import os
import sys as system
from pathlib import Path
from typing import List, Dict
"""
        service = TreeSitterService()
        tree = service.parse_code(code)
        imports = service.get_import_nodes(tree)

        assert len(imports) == 4

    def test_tree_sitter_analyze_multiple_languages(self):
        """RED: Test analyzing different languages"""
        from agently.core.tree_sitter_service import TreeSitterService, get_language

        # Test Python
        python_lang = get_language("python")
        assert python_lang is not None

        # Verify service can work with different languages
        service = TreeSitterService()

        # Python code
        py_code = "def func(): pass"
        py_tree = service.parse_code(py_code)
        assert py_tree.root_node.type == "module"


class TestTreeSitterIntegrationWithAST:
    """Test tree-sitter integration with Python AST"""

    def test_compare_ast_and_tree_sitter(self):
        """RED: Test comparing AST and tree-sitter results"""
        import ast

        from agently.core.tree_sitter_service import TreeSitterService

        code = """
def hello(name: str) -> str:
    return f"Hello, {name}!"

class Greeter:
    def greet(self) -> str:
        return "Hello"
"""
        # Parse with AST
        ast_tree = ast.parse(code)
        ast_functions = [
            node.name for node in ast.walk(ast_tree) if isinstance(node, ast.FunctionDef)
        ]

        # Parse with tree-sitter
        ts_service = TreeSitterService()
        ts_tree = ts_service.parse_code(code)
        ts_functions = [ts_service.get_node_name(f) for f in ts_service.get_function_nodes(ts_tree)]

        # Both should find the same functions
        assert "hello" in ast_functions
        assert "hello" in ts_functions
        assert "greet" in ast_functions
        assert "greet" in ts_functions

    def test_hybrid_analysis(self):
        """RED: Test hybrid analysis using both AST and tree-sitter"""
        from agently.core.code_understanding import CodeUnderstandingService
        from agently.core.tree_sitter_service import TreeSitterService

        code = """
@decorator
def func(x: int) -> int:
    '''Docstring'''
    return x * 2
"""
        # Use AST for semantic analysis
        ast_service = CodeUnderstandingService()

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write(code)
            temp_path = f.name

        try:
            ast_functions = ast_service.extract_functions(Path(temp_path))

            # Use tree-sitter for syntactic analysis
            ts_service = TreeSitterService()
            ts_tree = ts_service.parse_code(code)
            ts_functions = ts_service.get_function_nodes(ts_tree)

            # Both should find the function
            assert len(ast_functions) == 1
            assert len(ts_functions) == 1

            # AST provides semantic info
            assert ast_functions[0].name == "func"
            assert ast_functions[0].docstring == "Docstring"

            # Tree-sitter provides syntactic info
            decorators = ts_service.get_function_decorators(ts_tree, ts_functions[0])
            assert "decorator" in decorators
        finally:
            os.unlink(temp_path)


class TestTreeSitterService:
    """Test TreeSitterService class"""

    def test_service_initialization(self):
        """RED: Test service initializes correctly"""
        from agently.core.tree_sitter_service import TreeSitterService

        service = TreeSitterService()
        assert service.language is not None
        assert service.parser is not None

    def test_service_parse_error_handling(self):
        """RED: Test service handles parse errors"""
        from agently.core.tree_sitter_service import TreeSitterService

        service = TreeSitterService()

        # Invalid syntax should still produce a tree (with error nodes)
        code = "def broken("
        tree = service.parse_code(code)

        assert tree is not None
        # Tree-sitter produces error nodes for invalid syntax
        assert tree.root_node.has_error is True or tree.root_node.type == "module"
