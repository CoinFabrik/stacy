from tree_sitter import Node
from stacy_analyzer.visitor import Visitor
from stacy_analyzer.node_iterator import NodeIterator


class UnusedArguments(Visitor):

    def __init__(self, print_output: bool = True):
        super().__init__(print_output)

    def visit_node(self, node: Node, i):
        arguments = {}

        if i > 1:
            return

        if node.grammar_name == "function_definition":
            # parameters' name
            for child in node.child(0).child(2).children:
                if child.grammar_name == "function_parameter":
                    argument = child.child(1).text.decode("utf-8")
                    arguments[argument] = child

            # function's body
            fn_body = node.child(0).children[3:]  # all but the fn name, signature and first (

            for child in fn_body:
                for gchild in NodeIterator(child):
                    if gchild.text.decode("utf-8") in arguments:
                        del arguments[gchild.text.decode("utf-8")]

            for k, v in arguments.items():
                self.MSG = f"'{k}' argument passed but not used."
                self.HELP = None
                self.FOOTNOTE = f"Consider removing '{k}' since its not used inside the function."
                self.add_finding(v, v)
