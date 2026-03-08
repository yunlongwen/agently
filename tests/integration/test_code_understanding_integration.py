"""Code Understanding Service Integration Tests

Tests for code understanding service with real Python files.
Following TDD: tests are written before implementation.
"""

import os
import tempfile
from pathlib import Path

import pytest


class TestCodeUnderstandingIntegration:
    """Test code understanding service with real files"""

    def test_parse_real_python_file(self):
        """RED: Test parsing a real Python file"""
        from agently.core.code_understanding import CodeUnderstandingService

        # Create temp Python file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("""
def hello(name: str) -> str:
    '''Greet someone'''
    return f"Hello, {name}!"

class Greeter:
    '''A greeter class'''

    def __init__(self, greeting: str = "Hello"):
        self.greeting = greeting

    def greet(self, name: str) -> str:
        return f"{self.greeting}, {name}!"
""")
            temp_path = f.name

        try:
            service = CodeUnderstandingService()
            tree = service.parse_python_code(Path(temp_path))

            assert tree is not None
            assert isinstance(tree.body, list)
        finally:
            os.unlink(temp_path)

    def test_extract_functions_from_real_file(self):
        """RED: Test extracting functions from real file"""
        from agently.core.code_understanding import CodeUnderstandingService

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("""
def add(a: int, b: int) -> int:
    '''Add two numbers'''
    return a + b

async def fetch_data(url: str) -> str:
    '''Fetch data from URL'''
    return "data"

def multiply(x, y):
    return x * y
""")
            temp_path = f.name

        try:
            service = CodeUnderstandingService()
            functions = service.extract_functions(Path(temp_path))

            assert len(functions) == 3
            func_names = [f.name for f in functions]
            assert "add" in func_names
            assert "fetch_data" in func_names
            assert "multiply" in func_names

            # Check function details
            add_func = next(f for f in functions if f.name == "add")
            assert add_func.args == ["a", "b"]
            assert add_func.docstring == "Add two numbers"
            assert add_func.is_async is False

            fetch_func = next(f for f in functions if f.name == "fetch_data")
            assert fetch_func.is_async is True
        finally:
            os.unlink(temp_path)

    def test_extract_classes_from_real_file(self):
        """RED: Test extracting classes from real file"""
        from agently.core.code_understanding import CodeUnderstandingService

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("""
class Animal:
    '''Base animal class'''

    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        raise NotImplementedError

class Dog(Animal):
    '''Dog class'''

    def __init__(self, name: str, breed: str):
        super().__init__(name)
        self.breed = breed

    def speak(self) -> str:
        return "Woof!"
""")
            temp_path = f.name

        try:
            service = CodeUnderstandingService()
            classes = service.extract_classes(Path(temp_path))

            assert len(classes) == 2
            class_names = [c.name for c in classes]
            assert "Animal" in class_names
            assert "Dog" in class_names

            # Check inheritance
            dog_class = next(c for c in classes if c.name == "Dog")
            assert "Animal" in dog_class.bases

            # Check methods
            animal_class = next(c for c in classes if c.name == "Animal")
            assert "speak" in animal_class.methods
        finally:
            os.unlink(temp_path)

    def test_get_file_structure(self):
        """RED: Test getting complete file structure"""
        from agently.core.code_understanding import CodeUnderstandingService

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("""
import os
from pathlib import Path

VERSION = "1.0.0"
DEBUG = True

def main():
    pass

class App:
    pass
""")
            temp_path = f.name

        try:
            service = CodeUnderstandingService()
            structure = service.get_file_structure(Path(temp_path))

            assert "imports" in structure
            assert "classes" in structure
            assert "functions" in structure
            assert "variables" in structure

            assert len(structure["imports"]) == 2
            assert len(structure["classes"]) == 1
            assert len(structure["functions"]) == 1
            assert len(structure["variables"]) == 2
        finally:
            os.unlink(temp_path)

    def test_get_detailed_structure(self):
        """RED: Test getting detailed structure with CodeStructure"""
        from agently.core.code_understanding import (
            CodeStructure,
            CodeUnderstandingService,
        )

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("""
\"\"\"Module docstring\"\"\"

def func1():
    pass

class Class1:
    pass
""")
            temp_path = f.name

        try:
            service = CodeUnderstandingService()
            structure = service.get_detailed_structure(Path(temp_path))

            assert isinstance(structure, CodeStructure)
            assert structure.docstring == "Module docstring"
            assert len(structure.functions) == 1
            assert len(structure.classes) == 1
            assert structure.total_lines > 0
        finally:
            os.unlink(temp_path)

    def test_analyze_dependencies(self):
        """RED: Test analyzing file dependencies"""
        from agently.core.code_understanding import CodeUnderstandingService

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("""
import os
import sys
from pathlib import Path
from typing import Optional

import requests
import numpy as np
""")
            temp_path = f.name

        try:
            service = CodeUnderstandingService()
            dependencies = service.analyze_dependencies(Path(temp_path))

            assert "os" in dependencies
            assert "sys" in dependencies
            assert "pathlib" in dependencies
            assert "typing" in dependencies
            assert "requests" in dependencies
            assert "numpy" in dependencies
        finally:
            os.unlink(temp_path)

    def test_find_symbol_definition(self):
        """RED: Test finding symbol definition"""
        from agently.core.code_understanding import CodeUnderstandingService

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("""
class MyClass:
    '''My class'''
    pass

def my_function():
    '''My function'''
    pass

my_var = 42
""")
            temp_path = f.name

        try:
            service = CodeUnderstandingService()

            # Find class
            class_info = service.find_symbol_definition(Path(temp_path), "MyClass")
            assert class_info is not None
            assert class_info["type"] == "class"
            assert class_info["docstring"] == "My class"

            # Find function
            func_info = service.find_symbol_definition(Path(temp_path), "my_function")
            assert func_info is not None
            assert func_info["type"] == "function"

            # Find variable
            var_info = service.find_symbol_definition(Path(temp_path), "my_var")
            assert var_info is not None
            assert var_info["type"] == "variable"
        finally:
            os.unlink(temp_path)

    def test_get_function_complexity(self):
        """RED: Test calculating function complexity"""
        from agently.core.code_understanding import CodeUnderstandingService

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("""
def simple_function():
    return 1

def complex_function(x):
    if x > 0:
        for i in range(x):
            if i % 2 == 0:
                print(i)
    elif x < 0:
        while x < 0:
            x += 1
    else:
        try:
            raise ValueError()
        except:
            pass
    return x and True or False
""")
            temp_path = f.name

        try:
            service = CodeUnderstandingService()

            simple_complexity = service.get_function_complexity(Path(temp_path), "simple_function")
            complex_complexity = service.get_function_complexity(
                Path(temp_path), "complex_function"
            )

            assert simple_complexity == 1  # Base complexity
            assert complex_complexity > simple_complexity
        finally:
            os.unlink(temp_path)

    def test_extract_docstrings(self):
        """RED: Test extracting all docstrings"""
        from agently.core.code_understanding import CodeUnderstandingService

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write('''
"""Module level docstring"""

def func1():
    """Function 1 docstring"""
    pass

class Class1:
    """Class 1 docstring"""

    def method1(self):
        """Method 1 docstring"""
        pass
''')
            temp_path = f.name

        try:
            service = CodeUnderstandingService()
            docstrings = service.extract_docstrings(Path(temp_path))

            assert len(docstrings) >= 3  # Module, func1, Class1 (method might not be included)
            assert "Module level docstring" in docstrings
            assert "Function 1 docstring" in docstrings
            assert "Class 1 docstring" in docstrings
        finally:
            os.unlink(temp_path)

    def test_get_call_graph(self):
        """RED: Test building call graph"""
        from agently.core.code_understanding import CodeUnderstandingService

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("""
def helper():
    pass

def process(data):
    helper()
    return data

def main():
    data = process("input")
    helper()
    return data
""")
            temp_path = f.name

        try:
            service = CodeUnderstandingService()
            call_graph = service.get_call_graph(Path(temp_path))

            assert "main" in call_graph
            assert "process" in call_graph
            assert "helper" in call_graph

            # main calls process and helper
            assert "process" in call_graph["main"]
            assert "helper" in call_graph["main"]

            # process calls helper
            assert "helper" in call_graph["process"]
        finally:
            os.unlink(temp_path)

    def test_find_usages(self):
        """RED: Test finding symbol usages"""
        from agently.core.code_understanding import CodeUnderstandingService

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("""
my_var = 1
result = my_var + 1
print(my_var)

def use_var():
    return my_var * 2
""")
            temp_path = f.name

        try:
            service = CodeUnderstandingService()
            usages = service.find_usages(Path(temp_path), "my_var")

            # Should find definition and multiple usages
            assert len(usages) >= 3
        finally:
            os.unlink(temp_path)


class TestCodeUnderstandingEdgeCases:
    """Test edge cases in code understanding"""

    def test_parse_empty_file(self):
        """RED: Test parsing empty file"""
        from agently.core.code_understanding import CodeUnderstandingService

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("")
            temp_path = f.name

        try:
            service = CodeUnderstandingService()
            structure = service.get_file_structure(Path(temp_path))

            assert structure["functions"] == []
            assert structure["classes"] == []
        finally:
            os.unlink(temp_path)

    def test_parse_syntax_error(self):
        """RED: Test handling syntax errors"""
        from agently.core.code_understanding import CodeUnderstandingService

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("def broken(")  # Syntax error
            temp_path = f.name

        try:
            service = CodeUnderstandingService()

            with pytest.raises(SyntaxError):
                service.parse_python_code(Path(temp_path))
        finally:
            os.unlink(temp_path)

    def test_nested_functions(self):
        """RED: Test extracting nested functions"""
        from agently.core.code_understanding import CodeUnderstandingService

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("""
def outer():
    def inner():
        pass
    return inner
""")
            temp_path = f.name

        try:
            service = CodeUnderstandingService()
            functions = service.extract_functions(Path(temp_path))

            # Should find both outer and inner
            assert len(functions) == 2
        finally:
            os.unlink(temp_path)

    def test_decorated_functions(self):
        """RED: Test extracting decorated functions"""
        from agently.core.code_understanding import CodeUnderstandingService

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("""
def decorator(func):
    return func

@decorator
def decorated_func():
    pass

@property
def prop(self):
    pass
""")
            temp_path = f.name

        try:
            service = CodeUnderstandingService()
            functions = service.extract_functions(Path(temp_path))

            decorated = next(f for f in functions if f.name == "decorated_func")
            assert "decorator" in decorated.decorators
        finally:
            os.unlink(temp_path)
