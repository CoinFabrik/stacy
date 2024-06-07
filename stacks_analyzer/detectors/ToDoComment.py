
from tree_sitter import Node

import re

from ..print_message import pretty_print_warn
from ..visitor import Visitor

class ToDoComment(Visitor):
    MSG = "Remove TODO: comment before deploying contract"
    comments: [] = []

    def __init__(self):
        super().__init__()
        self.comments: [] = []

    def visit_node(self, node: Node, run_number: int):

        if run_number == 1 and node.grammar_name == "comment":
            if "todo" in node.text.decode("utf-8").lower():
                self.comments.append(node)
            return

        if run_number == 3:
            for n in self.comments:
                pretty_print_warn(
                    self,
                    n,
                    n,
                    self.MSG,
                    None
                )
            self.comments = []
