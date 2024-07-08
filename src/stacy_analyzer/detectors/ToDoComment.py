from tree_sitter import Node
from stacy_analyzer.visitor import Visitor


class ToDoComment(Visitor):

    def __init__(self, print_output: bool = True):
        super().__init__(print_output)
        self.MSG = "Remove TODO: comment before deploying contract"
        self.HELP = None
        self.FOOTNOTE = None

    def visit_node(self, node: Node, run_number: int):

        if run_number == 1 and node.grammar_name == "comment":
            if "todo" in node.text.decode("utf-8").lower():
                self.add_finding(node, node)
