from tree_sitter import Node

from ..print_message import pretty_print_warn
from ..visitor import Visitor, NodeIterator


class CallInsideAsContract(Visitor):
    MSG = "Use of call-contract? inside an as-contract context."

    def __init__(self):
        super().__init__()
        self.call = False
        self.lit = False
        self.checked = []

    def visit_node(self, node: Node, i):
        if i > 1:
            pass
        if str(node.text, "utf8") == "as-contract":
            descendants = NodeIterator(node.parent)
            while True:
                n = descendants.next()
                if n is None:
                    break
                if str(n.text, "utf8") == "contract-call?":
                    self.call = True
                if n.grammar_name == "contract_principal_lit":
                    self.lit = True

            if (self.call and not self.lit) and node not in self.checked:
                pretty_print_warn(
                    self,
                    node.parent,
                    node,
                    self.MSG,
                    None,
                    None
                )
                self.checked.append(node)

        self.call = False
        self.lit = False
