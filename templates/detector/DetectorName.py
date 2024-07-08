from tree_sitter import Node
from stacy_analyzer.visitor import Visitor


class DetectorName(Visitor):
    
    """
    Implement the logic of your detector here
    """

    def __init__(self):
        super().__init__()
        self.MSG = "MSG"
        self.FOOTNOTE = "FOOTNOTE"
        self.HELP = "HELP" #optional

    def visit_node(self, node: Node, run_number: int):
        """
        Implement the logic of your detector here.
        Use the visitor's methods defined in coinfabrik/stacy/src/stacy_analyzer/visitor.py
        """
        if run_number == 1:
            pass

        if run_number == 2:
            pass

        if run_number == 3:
            pass
            
