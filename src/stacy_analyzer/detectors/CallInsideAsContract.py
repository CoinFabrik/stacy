from tree_sitter import Node

from stacy_analyzer.visitor import Visitor, NodeIterator


class CallInsideAsContract(Visitor):

    def __init__(self, print_output: bool = True):
        super().__init__(print_output)
        self.call = False
        self.lit = False
        self.checked = []
        self.MSG = "Use of call-contract? inside an as-contract context."
        self.HELP = None
        self.FOOTNOTE = None

    def visit_node(self, node: Node, i):
        if i > 1:
            pass
        if str(node.text, "utf8") == "as-contract":
            for n in NodeIterator(node.parent):
                if str(n.text, "utf8") == "contract-call?":
                    self.call = True
                if n.grammar_name == "contract_principal_lit":
                    self.lit = True

            if (self.call and not self.lit) and node not in self.checked:
                self.add_finding(node.parent, node)
                self.checked.append(node)

        self.call = False
        self.lit = False
