
from tree_sitter import Node

from ..print_message import pretty_print_warn
from ..visitor import Visitor, NodeIterator


class ArgumentsNotUsed(Visitor):
    def __init__(self):
        super().__init__()

    def visit_node(self, node: Node, run_number: int):
        arguments = {}
        if run_number == 1 and node.grammar_name in ["private_function", "read_only_function", "public_function"]:
            
            for child in node.children:

                if child.grammar_name == "function_signature":
                   #aca guardo todos los parametros que recibe la funcion
                    for grandchild in child.children:
                        if grandchild.grammar_name == "function_parameter":
                            arguments[grandchild.child(1).text.decode("utf-8")] = (0, child) #inicializo todos los argumetos en 0
                
                #el resto de la funcion esta adentro del let? CUANDO EXISTE UN LET EL CUERPO SIGUE ACA
                if child.grammar_name == "let_expression":
                    for grandchild in child.children:
                        #si no es local binding, ya tengo todo el cuerpo de mi funcion
                        if grandchild.grammar_name == "local_binding":
                            arguments[grandchild.child(1).text.decode("utf-8")] = (0, grandchild)
                        else:
                            for key in arguments:
                                update = arguments[key]
                                count = update[0] + grandchild.text.decode("utf-8").count(key)
                                arguments[key] = (count, update[1])

                elif child.grammar_name == "basic_native_form":
                    for grandchild in child.children:
                        for key in arguments:
                                update = arguments[key]
                                count = update[0] + grandchild.text.decode("utf-8").count(key)
                                arguments[key] = (count, update[1])

            print("arguments", arguments)
            for k, v in arguments.items():
                if v[0] == 0:
                    pretty_print_warn(
                        self,
                        v[1],
                        v[1],
                        f"'{k}' argument is not used." ,
                        None
                    )