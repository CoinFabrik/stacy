from tree_sitter import Node
from stacy_analyzer.visitor import Visitor, NodeIterator


class UnwrapPanicUsage(Visitor):

    def __init__(self):
        super().__init__()
        self.MSG = "Use of unwrap-panic."
        self.FOOTNOTE = "Use unwrap! and handle the error."
        self.HELP = None

    def visit_node(self, node: Node, i):
        if i > 1:
            return
        if node.grammar_name == "unwrap-panic":
            self.add_finding(node.parent, node)

