from tree_sitter import Node

from stacy_analyzer.visitor import Visitor


class UnwrapPanicUsage(Visitor):

    def __init__(self, print_output: bool = True):
        super().__init__(print_output)
        self.MSG = "Use of unwrap-panic."
        self.FOOTNOTE = "Use unwrap! and handle the error."
        self.HELP = None

    def visit_node(self, node: Node, i):
        if i > 1:
            return
        if node.grammar_name == "unwrap-panic":
            self.add_finding(node.parent, node)
