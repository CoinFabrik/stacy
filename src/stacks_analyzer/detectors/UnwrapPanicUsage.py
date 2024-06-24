from tree_sitter import Node

from ..print_message import pretty_print_warn
from ..visitor import Visitor, NodeIterator


class UnwrapPanicUsage(Visitor):
    MSG = "Use of unwrap-panic."

    def __init__(self):
        super().__init__()

    def visit_node(self, node: Node, i):
        if i > 1:
            return
        if node.grammar_name == "unwrap-panic":
            # pretty_print_warn(
            #     self,
            #     node.parent,
            #     node,
            #     self.MSG,
            #     None,
            #     "Use unwrap! and handle the error."
            # )
            self.add_finding(node.parent, self.MSG, "Use unwrap! and handle the error.")

