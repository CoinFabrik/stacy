from tree_sitter import Node
from stacy_analyzer.visitor import Visitor, NodeIterator

class UnusedArguments(Visitor):
   
    def __init__(self):
        super().__init__()



    def visit_node(self, node: Node, i):
        arguments = {}

        if i > 1:
            return
        
        if node.grammar_name == "function_definition":   

            #parameters' name
            for child in node.child(0).child(2).children:
                if child.grammar_name == "function_parameter":
                    argument = child.child(1).text.decode("utf-8")
                    arguments[argument] = child
                    
            #function's body
            fn_body = node.child(0).child(3)
            
            for child in NodeIterator(fn_body):
                if child.grammar_name == "identifier" and child.text.decode("utf-8") in arguments:
                    del arguments[child.text.decode("utf-8")]
                
            for k,v in arguments.items():
                self.MSG = f"'{k}' argument passed but not used."
                self.HELP = None
                self.FOOTNOTE = f"Consider removing '{k}' since its not used inside the function."
                self.add_finding(v, v)

