from tree_sitter import Node
from stacy_analyzer.visitor import Visitor, NodeIterator


class AssertBlockHeight(Visitor):

    def __init__(self):
        super().__init__()
        self.MSG = "Use of block-height inside a assert."
        self.HELP = None
        self.FOOTNOTE = "Consider using burn-block-height."

    def visit_node(self, node: Node, i):
        if i > 1:
            return
        if str(node.text, "utf8") == "asserts!":
            for n in NodeIterator(node.parent):
                if str(n.text, "utf8") == "block-height" and n.grammar_name == "global":
                    self.add_finding(node.parent, node)
                    break
