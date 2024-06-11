from tree_sitter import Node

from ..print_message import pretty_print_warn
from ..visitor import Visitor, NodeIterator


class VarCouldBeConstant(Visitor):
    MSG = "This can be a define-constant because it's never set"
    data_vars: []

    def __init__(self):
        super().__init__()
        self.data_vars = []

    def visit_node(self, node: Node, i):
        if i == 1:
            if node.grammar_name == "define-data-var":
                self.data_vars.append(node.next_sibling)

        if i == 2:
            if node.grammar_name == "var-set":
                name = node.parent.next_sibling.text
                for n in self.data_vars:
                    if n.text == name:
                        self.data_vars.remove(n)

        if i == 3:
            for n in self.data_vars:
                pretty_print_warn(
                    self,
                    n,
                    n,
                    self.MSG,
                    None,
                    None
                )
            self.data_vars = []
