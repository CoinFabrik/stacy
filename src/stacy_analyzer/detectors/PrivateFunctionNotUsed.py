from tree_sitter import Node

from stacy_analyzer.visitor import Visitor


class PrivateFunctionNotUsed(Visitor):
    private_fns_names: [Node] = []

    def __init__(self, print_output: bool = True):
        super().__init__(print_output)
        self.private_fns_names: [Node] = []
        self.MSG = "This private function is not used."
        self.FOOTNOTE = "Consider removing it."
        self.HELP = None

    def visit_node(self, node: Node, run_number: int):
        if run_number == 1 and node.grammar_name == "private_function":
            self.private_fns_names.append(node)
            return

        # this can be improved with a better grammar (if not, stx-get-balance and other
        # intrinsic functions will throw as "not used" because they are not defined in the file
        if run_number == 2:
            if node.grammar_name == "contract_function_call":
                for saved in self.private_fns_names:
                    if saved.child(2).child(1).text == node.child(1).text:
                        self.private_fns_names.remove(saved)
                        break

            if node.grammar_name == "fold" or node.grammar_name == "map" or node.grammar_name == "filter":
                for saved in self.private_fns_names:
                    if saved.child(2).child(1).text == node.parent.parent.child(2).text:
                        self.private_fns_names.remove(saved)

        if run_number == 3:
            for n in self.private_fns_names:
                self.add_finding(n, n)
            self.private_fns_names = []
