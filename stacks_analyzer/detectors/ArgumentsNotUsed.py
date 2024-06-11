
from tree_sitter import Node

from ..print_message import pretty_print_warn
from ..visitor import Visitor, NodeIterator


class ArgumentsNotUsed(Visitor):
    MSG = "This function receives arguments that are never used."

    def __init__(self):
        super().__init__()

    def visit_node(self, node: Node, run_number: int):

        arguments = {}
        if run_number == 1 and node.grammar_name in ["private_function", "read_only_function", "public_function"]:

            descendants = NodeIterator(node.parent)

            while True:
                n = descendants.next()
                if n is None:
                    break
                
                if n.grammar_name == "function_parameter":
                    key = n.child(1).text.decode("utf-8") #name       
                    arguments[key] = (0, n.child(1))

                
                if n.grammar_name == "identifier":
                    key = n.text.decode("utf-8")

                    if key in arguments:
                        updated_tuple = arguments[key]
                        updated_tuple = (updated_tuple[0] + 1, updated_tuple[1])
                        arguments[key] = updated_tuple

                    
            for k, v in arguments.items():
                if v[0] == 0:
                    pretty_print_warn(
                        self,
                        v[1],
                        v[1],
                        f"'{k}' argument is not used." ,
                        None
                    )

            