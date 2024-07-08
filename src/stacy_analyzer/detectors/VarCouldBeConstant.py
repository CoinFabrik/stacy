from tree_sitter import Node
from stacy_analyzer.visitor import Visitor


class VarCouldBeConstant(Visitor):
    data_vars: []

    def __init__(self, print_output: bool = True):
        super().__init__(print_output)
        self.data_vars = []
        self.MSG = "This can be a define-constant because it's never set"
        self.HELP = None
        self.FOOTNOTE = None

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
            for node in self.data_vars:
                self.add_finding(node, node)
            self.data_vars = []
