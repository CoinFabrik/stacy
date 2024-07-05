from tree_sitter import Node
from stacy_analyzer.visitor import Visitor, NodeIterator


class UnusedLetVariables(Visitor):
    arguments = {}

    def __init__(self, print_output: bool = True):
        super().__init__(print_output)

    def visit_node(self, node: Node, i):

        if i > 1:
            return

        if node.type == "let_expression":

            let_iterator = NodeIterator(node)

            for let_node in let_iterator:
                if let_node.grammar_name == "local_binding":
                    argument = let_node.child(1).text.decode("utf-8")
                    self.arguments[argument] = let_node

                if let_node.text.decode("utf-8") in self.arguments:
                    del self.arguments[let_node.text.decode("utf-8")]

            for (k, v) in self.arguments.items():
                self.MSG = f"'{k}' variable created but not used."
                self.HELP = ""
                self.FOOTNOTE = f"Consider removing '{k}' from let function since its not used."
                self.add_finding(v, v)
