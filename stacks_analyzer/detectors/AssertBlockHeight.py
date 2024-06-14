from tree_sitter import Node

from ..print_message import pretty_print_warn
from ..visitor import Visitor, NodeIterator


class AssertBlockHeight(Visitor):
    MSG = "Use of block-height inside a assert."
    HELP = "Consider using burn-block-height."

    def __init__(self):
        super().__init__()

    def visit_node(self, node: Node, i):
        if i > 1:
            return
        if str(node.text, "utf8") == "asserts!":
            for n in NodeIterator(node.parent):
                if str(n.text, "utf8") == "block-height" and n.grammar_name == "global":
                    pretty_print_warn(
                        self,
                        node.parent,
                        node,
                        self.MSG,
                        None,
                        self.HELP
                    )
                    break
