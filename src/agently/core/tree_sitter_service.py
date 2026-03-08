"""Tree-sitter Service for code analysis

Provides syntactic code analysis using tree-sitter.
"""

from typing import Any, Callable, Optional

import tree_sitter_python
from tree_sitter import Language, Node, Parser, Tree

from agently.logging import get_logger

logger = get_logger(__name__)


def get_language(language_name: str = "python") -> Optional[Language]:
    """Get tree-sitter language for the specified language

    Args:
        language_name: Name of the language

    Returns:
        Tree-sitter Language or None if not available
    """
    if language_name == "python":
        return Language(tree_sitter_python.language())
    return None


class TreeSitterService:
    """
    Tree-sitter Service - 代码语法分析服务

    使用 tree-sitter 进行代码语法树分析。
    """

    def __init__(self, language_name: str = "python"):
        """Initialize tree-sitter service

        Args:
            language_name: Language to use for parsing
        """
        self.language_name = language_name
        self._language = get_language(language_name)
        self.parser = Parser()

        if self._language:
            self.parser.language = self._language
            logger.info("Tree-sitter initialized", language=language_name)
        else:
            logger.warning(f"Language {language_name} not available")

    @property
    def language(self) -> Optional[Language]:
        """Get the language"""
        return self._language

    def parse_code(self, code: str) -> Tree:
        """Parse code into syntax tree

        Args:
            code: Source code to parse

        Returns:
            Tree-sitter Tree
        """
        logger.debug("Parsing code with tree-sitter")
        return self.parser.parse(bytes(code, "utf-8"))

    def get_root_node(self, tree: Tree) -> Node:
        """Get root node of tree

        Args:
            tree: Tree-sitter Tree

        Returns:
            Root node
        """
        return tree.root_node

    def get_function_nodes(self, tree: Tree) -> list[Node]:
        """Get all function definition nodes

        Args:
            tree: Tree-sitter Tree

        Returns:
            List of function nodes
        """
        nodes = []
        self._collect_function_nodes(tree.root_node, nodes)
        return nodes

    def _collect_function_nodes(self, node: Node, result: list[Node]) -> None:
        """Recursively collect function nodes, including decorated ones

        Args:
            node: Current node
            result: List to append matches to
        """
        if node.type == "function_definition":
            result.append(node)
        elif node.type == "decorated_definition":
            # For decorated definitions, the function_definition is a child
            for child in node.children:
                if child.type == "function_definition":
                    result.append(child)
                    break
        else:
            for child in node.children:
                self._collect_function_nodes(child, result)

    def get_class_nodes(self, tree: Tree) -> list[Node]:
        """Get all class definition nodes

        Args:
            tree: Tree-sitter Tree

        Returns:
            List of class nodes
        """
        return self.query_nodes(tree, "class_definition")

    def get_import_nodes(self, tree: Tree) -> list[Node]:
        """Get all import statement nodes

        Args:
            tree: Tree-sitter Tree

        Returns:
            List of import nodes
        """
        imports = []
        imports.extend(self.query_nodes(tree, "import_statement"))
        imports.extend(self.query_nodes(tree, "import_from_statement"))
        return imports

    def get_node_name(self, node: Node) -> str:
        """Get name of a node (function name, class name, etc.)

        Args:
            node: Tree-sitter Node

        Returns:
            Name string
        """
        if node.type == "function_definition":
            # Function name is in the first identifier child
            for child in node.children:
                if child.type == "identifier":
                    return child.text.decode("utf-8")
        elif node.type == "class_definition":
            # Class name is in the first identifier child
            for child in node.children:
                if child.type == "identifier":
                    return child.text.decode("utf-8")
        elif node.type == "identifier":
            return node.text.decode("utf-8")
        return ""

    def get_function_parameters(self, node: Node) -> list[dict[str, Any]]:
        """Get parameters of a function

        Args:
            node: Function definition node

        Returns:
            List of parameter info dictionaries
        """
        parameters = []

        # Find parameters node
        for child in node.children:
            if child.type == "parameters":
                for param in child.children:
                    if param.type == "identifier":
                        parameters.append(
                            {
                                "name": param.text.decode("utf-8"),
                                "type": None,
                            }
                        )
                    elif param.type == "typed_parameter":
                        # Typed parameter: name: type
                        name_node = None
                        type_node = None
                        for p_child in param.children:
                            if p_child.type == "identifier":
                                name_node = p_child
                            elif p_child.type == "type":
                                type_node = p_child
                        if name_node:
                            parameters.append(
                                {
                                    "name": name_node.text.decode("utf-8"),
                                    "type": type_node.text.decode("utf-8") if type_node else None,
                                }
                            )
                    elif param.type == "typed_default_parameter":
                        # Typed default parameter: name: type = value
                        name_node = None
                        type_node = None
                        for p_child in param.children:
                            if p_child.type == "identifier":
                                name_node = p_child
                            elif p_child.type == "type":
                                type_node = p_child
                        if name_node:
                            parameters.append(
                                {
                                    "name": name_node.text.decode("utf-8"),
                                    "type": type_node.text.decode("utf-8") if type_node else None,
                                    "default": True,
                                }
                            )
                    elif param.type == "default_parameter":
                        # Default parameter: name = value
                        name_node = param.child_by_field_name("name")
                        if name_node is None:
                            # Fallback: find identifier
                            for p_child in param.children:
                                if p_child.type == "identifier":
                                    name_node = p_child
                                    break
                        if name_node:
                            parameters.append(
                                {
                                    "name": name_node.text.decode("utf-8"),
                                    "type": None,
                                    "default": True,
                                }
                            )
                break

        return parameters

    def get_function_return_type(self, node: Node) -> Optional[str]:
        """Get return type annotation of a function

        Args:
            node: Function definition node

        Returns:
            Return type string or None
        """
        for child in node.children:
            if child.type == "type":
                # Check if this is a return type (comes after ->)
                prev_sibling = None
                for prev in node.children:
                    if prev is child:
                        break
                    prev_sibling = prev

                if prev_sibling and prev_sibling.type == "->":
                    return child.text.decode("utf-8")

        # Alternative: look for -> followed by type
        found_arrow = False
        for child in node.children:
            if found_arrow and child.type == "type":
                return child.text.decode("utf-8")
            if child.type == "->":
                found_arrow = True

        return None

    def get_function_decorators(self, tree: Tree, node: Node) -> list[str]:
        """Get decorators of a function

        Args:
            tree: Tree-sitter Tree
            node: Function definition node

        Returns:
            List of decorator names
        """
        decorators = []

        # Find the decorated_definition parent by walking the tree
        decorated_parent = self._find_decorated_parent(tree, node)

        if decorated_parent:
            for child in decorated_parent.children:
                if child.type == "decorator":
                    for dec_child in child.children:
                        if dec_child.type == "identifier":
                            decorators.append(dec_child.text.decode("utf-8"))
                        elif dec_child.type == "call":
                            for call_child in dec_child.children:
                                if call_child.type == "identifier":
                                    decorators.append(call_child.text.decode("utf-8"))

        return decorators

    def _find_decorated_parent(self, tree: Tree, target_node: Node) -> Optional[Node]:
        """Find decorated_definition parent of a function node

        Args:
            tree: Tree-sitter Tree
            target_node: Function definition node

        Returns:
            decorated_definition node or None
        """

        def search(node: Node, parent: Optional[Node]) -> Optional[Node]:
            if node is target_node:
                return parent if parent and parent.type == "decorated_definition" else None

            for child in node.children:
                result = search(child, node if node.type == "decorated_definition" else parent)
                if result:
                    return result
            return None

        # Special handling: check if target is inside a decorated_definition
        for child in tree.root_node.children:
            if child.type == "decorated_definition":
                for grandchild in child.children:
                    if grandchild.type == "function_definition":
                        # Check if this is our target by comparing positions
                        if (
                            grandchild.start_point == target_node.start_point
                            and grandchild.end_point == target_node.end_point
                        ):
                            return child
        return None

    def get_class_bases(self, node: Node) -> list[Node]:
        """Get base classes of a class

        Args:
            node: Class definition node

        Returns:
            List of base class nodes
        """
        bases = []

        # Look for argument_list after class name (contains base classes)
        found_name = False
        for child in node.children:
            if found_name:
                if child.type == "argument_list":
                    for arg in child.children:
                        if arg.type == "identifier":
                            bases.append(arg)
                elif child.type == ":":
                    break
            elif child.type == "identifier":
                found_name = True

        return bases

    def get_docstring(self, node: Node) -> Optional[str]:
        """Get docstring from a node

        Args:
            node: Node that may contain a docstring

        Returns:
            Docstring content or None
        """
        # Look for expression_statement with string as first child in block
        for child in node.children:
            if child.type == "block":
                # First child of block might be docstring
                for block_child in child.children:
                    if block_child.type == "expression_statement":
                        for expr_child in block_child.children:
                            if expr_child.type == "string":
                                # Get string_content from inside string
                                for string_child in expr_child.children:
                                    if string_child.type == "string_content":
                                        return string_child.text.decode("utf-8")
        return None

    def query_nodes(self, tree: Tree, node_type: str) -> list[Node]:
        """Query all nodes of a specific type

        Args:
            tree: Tree-sitter Tree
            node_type: Type of nodes to find

        Returns:
            List of matching nodes
        """
        nodes = []
        self._collect_nodes(tree.root_node, node_type, nodes)
        return nodes

    def _collect_nodes(self, node: Node, node_type: str, result: list[Node]) -> None:
        """Recursively collect nodes of specific type

        Args:
            node: Current node
            node_type: Type to match
            result: List to append matches to
        """
        if node.type == node_type:
            result.append(node)

        for child in node.children:
            self._collect_nodes(child, node_type, result)

    def walk_tree(self, node: Node, visitor: Callable[[Node], None]) -> None:
        """Walk tree and visit each node

        Args:
            node: Starting node
            visitor: Function to call on each node
        """
        visitor(node)
        for child in node.children:
            self.walk_tree(child, visitor)

    def find_node_at_position(self, tree: Tree, line: int, column: int) -> Optional[Node]:
        """Find node at specific position

        Args:
            tree: Tree-sitter Tree
            line: Line number (1-based)
            column: Column number (0-based)

        Returns:
            Node at position or None
        """
        # Convert to byte position (tree-sitter uses 0-based row, column)
        return tree.root_node.descendant_for_point_range((line - 1, column), (line - 1, column))

    def get_node_text(self, node: Node, source_code: bytes) -> str:
        """Get source text for a node

        Args:
            node: Tree-sitter Node
            source_code: Original source code as bytes

        Returns:
            Source text for the node
        """
        start_byte = node.start_byte
        end_byte = node.end_byte
        return source_code[start_byte:end_byte].decode("utf-8")

    def get_node_range(self, node: Node) -> dict[str, int]:
        """Get source range for a node

        Args:
            node: Tree-sitter Node

        Returns:
            Dictionary with start/end line and column
        """
        return {
            "start_line": node.start_point[0] + 1,
            "start_column": node.start_point[1],
            "end_line": node.end_point[0] + 1,
            "end_column": node.end_point[1],
        }

    def get_all_identifiers(self, tree: Tree) -> list[str]:
        """Get all identifiers in the tree

        Args:
            tree: Tree-sitter Tree

        Returns:
            List of identifier names
        """
        identifiers = []
        nodes = self.query_nodes(tree, "identifier")
        for node in nodes:
            identifiers.append(node.text.decode("utf-8"))
        return identifiers

    def get_assignment_targets(self, tree: Tree) -> list[dict[str, Any]]:
        """Get all assignment targets

        Args:
            tree: Tree-sitter Tree

        Returns:
            List of assignment info dictionaries
        """
        assignments = []
        nodes = self.query_nodes(tree, "assignment")

        for node in nodes:
            left_node = node.child_by_field_name("left")
            right_node = node.child_by_field_name("right")

            if left_node:
                assignments.append(
                    {
                        "target": left_node.text.decode("utf-8"),
                        "value": right_node.text.decode("utf-8") if right_node else None,
                        "line": node.start_point[0] + 1,
                    }
                )

        return assignments

    def get_call_nodes(self, tree: Tree) -> list[dict[str, Any]]:
        """Get all function call nodes

        Args:
            tree: Tree-sitter Tree

        Returns:
            List of call info dictionaries
        """
        calls = []
        nodes = self.query_nodes(tree, "call")

        for node in nodes:
            func_node = node.child_by_field_name("function")
            if func_node:
                calls.append(
                    {
                        "function": func_node.text.decode("utf-8"),
                        "line": node.start_point[0] + 1,
                        "arguments": [
                            arg.text.decode("utf-8")
                            for arg in node.child_by_field_name("arguments").children
                            if arg.type != ","
                        ]
                        if node.child_by_field_name("arguments")
                        else [],
                    }
                )

        return calls
