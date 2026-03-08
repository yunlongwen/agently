"""Code understanding service using Python AST and tree-sitter"""

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from agently.logging import get_logger

logger = get_logger(__name__)


@dataclass
class FunctionInfo:
    """Information about a function"""

    name: str
    args: list[str] = field(default_factory=list)
    returns: Optional[str] = None
    docstring: Optional[str] = None
    line_start: int = 0
    line_end: int = 0
    decorators: list[str] = field(default_factory=list)
    is_async: bool = False
    is_method: bool = False


@dataclass
class ClassInfo:
    """Information about a class"""

    name: str
    bases: list[str] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)
    docstring: Optional[str] = None
    line_start: int = 0
    line_end: int = 0
    attributes: list[str] = field(default_factory=list)
    decorators: list[str] = field(default_factory=list)


@dataclass
class ImportInfo:
    """Information about an import"""

    module: str
    names: list[str] = field(default_factory=list)
    alias: Optional[str] = None
    is_from: bool = False
    line: int = 0


@dataclass
class VariableInfo:
    """Information about a variable"""

    name: str
    value: Optional[str] = None
    line: int = 0
    scope: str = "module"


@dataclass
class CodeStructure:
    """Complete structure of a code file"""

    file_path: str
    imports: list[ImportInfo] = field(default_factory=list)
    classes: list[ClassInfo] = field(default_factory=list)
    functions: list[FunctionInfo] = field(default_factory=list)
    variables: list[VariableInfo] = field(default_factory=list)
    docstring: Optional[str] = None
    total_lines: int = 0


class CodeUnderstandingService:
    """
    Code Understanding Service - 代码理解服务

    使用Python AST和tree-sitter分析代码结构。
    """

    def parse_python_code(self, file_path: Path) -> ast.AST:
        """
        Parse Python code into AST

        Args:
            file_path: Path to Python file

        Returns:
            AST of the Python code

        Raises:
            SyntaxError: If code has syntax errors
        """
        logger.info("Parsing Python code", file_path=str(file_path))
        code = file_path.read_text()
        return ast.parse(code)

    def extract_functions(self, file_path: Path) -> list[FunctionInfo]:
        """
        Extract function definitions from code

        Args:
            file_path: Path to Python file

        Returns:
            List of function information
        """
        logger.info("Extracting functions", file_path=str(file_path))
        tree = self.parse_python_code(file_path)
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                func_info = FunctionInfo(
                    name=node.name,
                    args=[arg.arg for arg in node.args.args],
                    line_start=node.lineno,
                    line_end=node.end_lineno or node.lineno,
                    docstring=ast.get_docstring(node),
                    is_async=isinstance(node, ast.AsyncFunctionDef),
                    is_method=self._is_method(node, tree),
                    decorators=[
                        d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list
                    ],
                )

                # Get return annotation
                if node.returns:
                    func_info.returns = (
                        ast.unparse(node.returns) if hasattr(ast, "unparse") else str(node.returns)
                    )

                functions.append(func_info)

        return functions

    def _is_method(self, func_node: ast.FunctionDef, tree: ast.AST) -> bool:
        """Check if function is a method inside a class"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if item is func_node:
                        return True
        return False

    def extract_classes(self, file_path: Path) -> list[ClassInfo]:
        """
        Extract class definitions from code

        Args:
            file_path: Path to Python file

        Returns:
            List of class information
        """
        logger.info("Extracting classes", file_path=str(file_path))
        tree = self.parse_python_code(file_path)
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = ClassInfo(
                    name=node.name,
                    bases=[self._get_name(base) for base in node.bases],
                    methods=[n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                    docstring=ast.get_docstring(node),
                    line_start=node.lineno,
                    line_end=node.end_lineno or node.lineno,
                    decorators=[
                        d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list
                    ],
                )

                # Extract class attributes
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                class_info.attributes.append(target.id)

                classes.append(class_info)

        return classes

    def _get_name(self, node: ast.AST) -> str:
        """Get name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            return self._get_name(node.value)
        return str(node)

    def get_file_structure(self, file_path: Path) -> dict[str, Any]:
        """
        Get complete structure of a Python file

        Args:
            file_path: Path to Python file

        Returns:
            Dictionary with classes, functions, imports
        """
        logger.info("Getting file structure", file_path=str(file_path))
        tree = self.parse_python_code(file_path)

        structure: dict[str, Any] = {
            "classes": [],
            "functions": [],
            "imports": [],
            "variables": [],
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                structure["classes"].append(node.name)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not self._is_method(node, tree):
                    structure["functions"].append(node.name)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        structure["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    structure["imports"].append(node.module)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        structure["variables"].append(target.id)

        return structure

    def get_detailed_structure(self, file_path: Path) -> CodeStructure:
        """
        Get detailed structure of a Python file

        Args:
            file_path: Path to Python file

        Returns:
            CodeStructure with detailed information
        """
        logger.info("Getting detailed structure", file_path=str(file_path))
        tree = self.parse_python_code(file_path)
        code = file_path.read_text()

        structure = CodeStructure(
            file_path=str(file_path),
            imports=self.get_imports(file_path),
            classes=self.extract_classes(file_path),
            functions=[f for f in self.extract_functions(file_path) if not f.is_method],
            variables=self._extract_variables(tree),
            docstring=ast.get_docstring(tree),
            total_lines=len(code.splitlines()),
        )

        return structure

    def _extract_variables(self, tree: ast.AST) -> list[VariableInfo]:
        """Extract module-level variables"""
        variables = []

        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_info = VariableInfo(
                            name=target.id,
                            line=node.lineno,
                            scope="module",
                        )
                        if hasattr(ast, "unparse"):
                            var_info.value = ast.unparse(node.value)
                        variables.append(var_info)

        return variables

    def get_imports(self, file_path: Path) -> list[ImportInfo]:
        """
        Get all imports from a file

        Args:
            file_path: Path to Python file

        Returns:
            List of import information
        """
        tree = self.parse_python_code(file_path)
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(
                        ImportInfo(
                            module=alias.name,
                            names=[alias.name],
                            alias=alias.asname,
                            is_from=False,
                            line=node.lineno,
                        )
                    )
            elif isinstance(node, ast.ImportFrom):
                names = [alias.name for alias in node.names]
                imports.append(
                    ImportInfo(
                        module=node.module or "",
                        names=names,
                        is_from=True,
                        line=node.lineno,
                    )
                )

        return imports

    def analyze_dependencies(self, file_path: Path) -> set[str]:
        """
        Analyze dependencies of a file

        Args:
            file_path: Path to Python file

        Returns:
            Set of dependency module names
        """
        imports = self.get_imports(file_path)
        dependencies = set()

        for imp in imports:
            # Get the top-level module
            top_module = imp.module.split(".")[0] if imp.module else ""
            if top_module:
                dependencies.add(top_module)
            for name in imp.names:
                if name and not name.startswith("."):
                    dependencies.add(name.split(".")[0])

        return dependencies

    def find_symbol_definition(self, file_path: Path, symbol_name: str) -> Optional[dict[str, Any]]:
        """
        Find the definition of a symbol

        Args:
            file_path: Path to Python file
            symbol_name: Name of the symbol to find

        Returns:
            Symbol definition info or None
        """
        tree = self.parse_python_code(file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == symbol_name:
                return {
                    "name": node.name,
                    "type": "class",
                    "line": node.lineno,
                    "docstring": ast.get_docstring(node),
                }
            elif (
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name == symbol_name
            ):
                return {
                    "name": node.name,
                    "type": "function",
                    "line": node.lineno,
                    "docstring": ast.get_docstring(node),
                }
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == symbol_name:
                        return {
                            "name": target.id,
                            "type": "variable",
                            "line": node.lineno,
                        }

        return None

    def get_function_complexity(self, file_path: Path, function_name: str) -> int:
        """
        Calculate cyclomatic complexity of a function

        Args:
            file_path: Path to Python file
            function_name: Name of the function

        Returns:
            Cyclomatic complexity (1 = simple, higher = more complex)
        """
        tree = self.parse_python_code(file_path)
        complexity = 1  # Base complexity

        for node in ast.walk(tree):
            if (
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name == function_name
            ):
                # Count decision points
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                        complexity += 1
                    elif isinstance(child, ast.BoolOp):
                        # and/or operators add complexity
                        complexity += len(child.values) - 1
                    elif isinstance(child, ast.comprehension):
                        complexity += 1
                        if child.ifs:
                            complexity += len(child.ifs)

                return complexity

        return complexity

    def extract_docstrings(self, file_path: Path) -> list[str]:
        """
        Extract all docstrings from a file

        Args:
            file_path: Path to Python file

        Returns:
            List of docstrings
        """
        tree = self.parse_python_code(file_path)
        docstrings = []

        # Module docstring
        module_doc = ast.get_docstring(tree)
        if module_doc:
            docstrings.append(module_doc)

        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                doc = ast.get_docstring(node)
                if doc:
                    docstrings.append(doc)

        return docstrings

    def get_call_graph(self, file_path: Path) -> dict[str, list[str]]:
        """
        Build a simple call graph

        Args:
            file_path: Path to Python file

        Returns:
            Dictionary mapping function names to their called functions
        """
        tree = self.parse_python_code(file_path)
        call_graph: dict[str, list[str]] = {}

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                calls = []
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Name):
                            calls.append(child.func.id)
                        elif isinstance(child.func, ast.Attribute):
                            calls.append(child.func.attr)
                call_graph[node.name] = list(set(calls))

        return call_graph

    def find_usages(self, file_path: Path, symbol_name: str) -> list[dict[str, Any]]:
        """
        Find usages of a symbol in the file

        Args:
            file_path: Path to Python file
            symbol_name: Name of the symbol to find usages for

        Returns:
            List of usage locations
        """
        tree = self.parse_python_code(file_path)
        usages = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id == symbol_name:
                usages.append(
                    {
                        "line": node.lineno,
                        "col": node.col_offset,
                        "context": "reference",
                    }
                )
            elif isinstance(node, ast.Attribute) and node.attr == symbol_name:
                usages.append(
                    {
                        "line": node.lineno,
                        "col": node.col_offset,
                        "context": "attribute",
                    }
                )

        return usages
