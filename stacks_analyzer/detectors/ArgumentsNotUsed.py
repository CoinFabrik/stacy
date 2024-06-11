
from tree_sitter import Node

from ..print_message import pretty_print_warn
from ..visitor import Visitor, NodeIterator


class ArgumentsNotUsed(Visitor):
    MSG = "This function receives arguments that are never used."
    
    #read_only_names: [Node] = []

    def __init__(self):
        super().__init__()

    def visit_node(self, node: Node, run_number: int):
        #si estoy en una funcion
        if run_number == 1 and node.grammar_name in ["private_function", "read_only_function", "public_function"]:
            body = node.text.decode("utf-8") #body function text
            signature = node.child(2) #save function signature

            # signature.child_count - 1 because the las child is ')'
            for i in range(1, signature.child_count - 1):
                print(signature.child(i).text, "signature child")
                if i != 1:
                    identifier = signature.child(i).child(1)

                    print(identifier.text, "identifier text~")

            