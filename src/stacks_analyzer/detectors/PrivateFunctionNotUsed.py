
from tree_sitter import Node

from ..print_message import pretty_print_warn
from ..visitor import Visitor, NodeIterator


class PrivateFunctionNotUsed(Visitor):
    MSG = "This private function is not used."
    private_fns_names: [Node] = []

    def __init__(self):
        super().__init__()
        self.private_fns_names: [Node] = []

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
                # pretty_print_warn(
                #     self,
                #     n,
                #     n,
                #     self.MSG,
                #     None,
                #     "Consider removing it."
                # )
                self.add_finding(n, self.MSG, None)
            self.private_fns_names = []
