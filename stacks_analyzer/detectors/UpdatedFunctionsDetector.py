from tree_sitter import Node

from ..print_message import pretty_print_warn
from ..visitor import Visitor


class UpdatedFunctionsDetector(Visitor):
    functions_updated = ["element-at", "index-of"]

    def __init__(self):
        super().__init__()

    def visit_node(self, node: Node, i):
        if i > 1:
            return
        
        fun = str(node.text, "utf-8")

        if fun in self.functions_updated:
            MSG = f"Behavior of '{fun}' changed from Clarity1 to Clarity2, now outputs optional value."
            pretty_print_warn(
                self,
                node.parent,
                node,
                MSG,
                None,
                f"Suggestion: use '{fun}?' to make this behavior explicit."
            )

