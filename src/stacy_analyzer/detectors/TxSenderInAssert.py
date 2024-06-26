from tree_sitter import Node

from stacy_analyzer.visitor import Visitor, NodeIterator


class TxSenderInAssert(Visitor):

    def __init__(self):
        super().__init__()
        self.MSG = "Use of tx-sender inside an assert"
        self.FOOTNOTE = "Consider using contract-caller."
        self.HELP = None

    def visit_node(self, node: Node, i):
        if i > 1:
            return
        if str(node.text, "utf8") == "asserts!":
            for n in NodeIterator(node.parent):
                if str(n.text, "utf8") == "tx-sender" and n.grammar_name == "global":
                    self.add_finding(node.parent, node)
                    break
