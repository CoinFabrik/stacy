from tree_sitter import Node
from stacy_analyzer.visitor import Visitor

"""
IMPORTANT: FALSE POSITIVES FOR ARGUMENTS INSIDE A (LET ) BODY

"""


class UnusedArguments(Visitor):
   
    def __init__(self):
        super().__init__()


    def visit_node(self, node: Node, i):
        
        if i > 1:
            return
        
        if i == 1 and node.grammar_name in ["private_function", "read_only_function", "public_function"]:
            arguments = {}
            for child in node.children:
                if child.grammar_name == "function_signature":
                    #save all arguments that are passed to the function
                    
                    for grandchild in child.children:
                        if grandchild.grammar_name == "function_parameter":
                            argument = grandchild.child(1).text.decode("utf-8")
                            arguments[argument] = (0, grandchild) 

                    
                if child.grammar_name == "basic_native_form":

                    for grandchild in child.children:
                        for key in arguments:
                            update = arguments[key] #update = (count, node)
                            count = update[0] + grandchild.text.decode("utf-8").count(key)
                            arguments[key] = (count, update[1])
            
            for k,v in arguments.items():

                #tuples are dict[argument] = (count, node)
                self.MSG = f"'{k}' argument passed but not used."
                self.HELP = None
                self.FOOTNOTE = f"Consider removing '{k}' since its not used inside the function."

                if v[0] == 0:
                    self.add_finding(v[1], v[1])
                
