from tree_sitter import Node

from ..print_message import pretty_print_warn
from ..visitor import Visitor, NodeIterator


class DivideBeforeMultiply(Visitor):
    MSG = "Use of divide inside a multiplication. This could result in a precision loss."
    NOTE = "Try multiplication before division."

    def __init__(self):
        super().__init__()

    def visit_node(self, node: Node, i):
        if i > 1:
            return
        if node.grammar_name == "native_identifier" and str(node.text, "utf8") == "*":
            descendants = NodeIterator(node.parent)
            while True:
                n = descendants.next()
                if n is None:
                    break
                if str(n.text, "utf8") == "/" and n.grammar_name == "native_identifier":
                    pretty_print_warn(
                        self,
                        node.parent,
                        node,
                        self.MSG,
                        None,
                        self.NOTE,
                    )