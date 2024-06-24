from tree_sitter import Node

from ..print_message import pretty_print_warn
from ..visitor import Visitor, NodeIterator


class TxSenderInAssert(Visitor):
    MSG = "Use of tx-sender inside an assert"

    def __init__(self):
        super().__init__()

    def visit_node(self, node: Node, i):
        if i > 1:
            return
        if str(node.text, "utf8") == "asserts!":
            for n in NodeIterator(node.parent):
                if str(n.text, "utf8") == "tx-sender" and n.grammar_name == "global":
                    # pretty_print_warn(
                    #     self,
                    #     node.parent,
                    #     node,
                    #     self.MSG,
                    #     None,
                    #     "Consider using contract-caller"
                    # )
                    self.add_finding(node.parent, self.MSG, "Consider using contract-caller.")
                    break

