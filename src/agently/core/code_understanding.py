"""Code understanding service using Python AST"""

import ast
from pathlib import Path
from typing import Any, List, Dict

from agently.logging import LoggingMixin


class CodeUnderstandingService(LoggingMixin):
    """Service for understanding code structure"""

    def parse_python_code(self, file_path: Path) -> ast.AST:
        """Parse Python code into AST

        Args:
            file_path: Path to Python file

        Returns:
            AST of the Python code

        Raises:
            SyntaxError: If code has syntax errors
        """
        self.logger.info("Parsing Python code", file_path=str(file_path))
        code = file_path.read_text()
        return ast.parse(code)

    def extract_functions(self, file_path: Path) -> List[ast.FunctionDef]:
        """Extract function definitions from code

        Args:
            file_path: Path to Python file

        Returns:
            List of function definitions
        """
        self.logger.info("Extracting functions", file_path=str(file_path))
        tree = self.parse_python_code(file_path)
        functions = []

        # First, get all top-level functions
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                functions.append(node)
            elif isinstance(node, ast.ClassDef):
                # Get methods from classes
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        functions.append(item)

        return functions

    def extract_classes(self, file_path: Path) -> List[ast.ClassDef]:
        """Extract class definitions from code

        Args:
            file_path: Path to Python file

        Returns:
            List of class definitions
        """
        self.logger.info("Extracting classes", file_path=str(file_path))
        tree = self.parse_python_code(file_path)
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node)

        return classes

    def get_file_structure(self, file_path: Path) -> Dict[str, Any]:
        """Get complete structure of a Python file

        Args:
            file_path: Path to Python file

        Returns:
            Dictionary with classes, functions, imports
        """
        self.logger.info("Getting file structure", file_path=str(file_path))
        tree = self.parse_python_code(file_path)

        structure: Dict[str, Any] = {
            "classes": [],
            "functions": [],
            "imports": [],
        }

        structure["functions"] = [f.name for f in self.extract_functions(file_path)]
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                structure["classes"].append(node.name)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        structure["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    structure["imports"].append(node.module)

        return structure
