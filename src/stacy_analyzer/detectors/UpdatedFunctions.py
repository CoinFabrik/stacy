from tree_sitter import Node
from stacy_analyzer.visitor import Visitor


class UpdatedFunctions(Visitor):
    functions_updated = ["element-at", "index-of"]

    def __init__(self):
        super().__init__()
        self.HELP = None

    def visit_node(self, node: Node, i):
        if i > 1:
            return
        
        fun = str(node.text, "utf-8")

        if fun in self.functions_updated:
            self.MSG = f"Behavior of '{fun}' changed from Clarity1 to Clarity2, now outputs optional value."
            self.FOOTNOTE = f"Suggestion: use '{fun}?' to make this behavior explicit."
            self.add_finding(node.parent, node)

