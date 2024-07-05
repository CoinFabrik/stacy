from tree_sitter import Node

from stacy_analyzer.visitor import Visitor, NodeIterator


class DivideBeforeMultiply(Visitor):

    def __init__(self, print_output: bool = True):
        super().__init__(print_output)
        self.MSG = "Use of divide inside a multiplication. This could result in a precision loss."
        self.FOOTNOTE = "Try multiplication before division."
        self.HELP = None

    def visit_node(self, node: Node, i):
        if i > 1:
            return
        if node.grammar_name == "native_identifier" and str(node.text, "utf8") == "*":
            for n in NodeIterator(node.parent):
                if str(n.text, "utf8") == "/" and n.grammar_name == "native_identifier":
                    self.add_finding(node.parent, node)
