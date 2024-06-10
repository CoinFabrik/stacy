
from tree_sitter import Node

from ..print_message import pretty_print_warn
from ..visitor import Visitor

class ToDoComment(Visitor):
    MSG = "Remove TODO: comment before deploying contract"

    def __init__(self):
        super().__init__()

    def visit_node(self, node: Node, run_number: int):

        if run_number == 1 and node.grammar_name == "comment":
            if "todo" in node.text.decode("utf-8").lower():
                pretty_print_warn(
                    self,
                    node,
                    node,
                    self.MSG,
                    None
                )

