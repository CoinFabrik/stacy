from tree_sitter import Node

from ..print_message import pretty_print_warn
from ..visitor import Visitor


class UpdatedFunctionsDetector(Visitor):
    MSG = ""
    functions_updated = ["element-at", "index-of"]

    def __init__(self):
        super().__init__()
        self.fun = ""

    def visit_node(self, node: Node, i):
        if i > 1:
            return
        
        self.fun = str(node.text, "utf-8")

        if self.fun in self.functions_updated:
            MSG = f"Behavior of '{self.fun}' changed from Clarity1 to Clarity2, now outputs optional value.\nSuggestion: use '{self.fun}?' to make this behavior explicit."
            pretty_print_warn(
                self,
                node.parent,
                node,
                MSG,
                None
            )

