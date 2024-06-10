from tree_sitter import Node

from ..print_message import pretty_print_warn
from ..visitor import Visitor

#default addresses of Clarity in devnet
known_principals = ['ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM',
                  'ST1SJ3DTE5DN7X54YDH5D64R3BCB6A2AG2ZQ8YPD5',
                  'ST2CY5V39NHDPWSXMW9QDT3HC3GD6Q6XX4CFRK9AG',
                  'ST2JHG361ZXG51QTKY2NQCVBPPRRE2KZB1HR05NNC',
                  'ST2NEB84ASENDXKYGJPQW86YXQCEFEX2ZQPG87ND',
                  'ST2REHHS5J3CERCRBEPMGH7921Q6PYKAADT7JP2VB',
                  'ST3AM1A56AK2C1XAFJ4115ZSV26EB49BVQ10MGCS0',
                  'ST3PF13W7Z0RRM42A8VZRVFQ75SV1K26RXEP8YGKJ',
                  'ST3NBRSFKX28FQ2ZJ1MAKX58HKHSDGNV5N7R21XCP',
                  'STNHKEPYEPJ8ET55ZZ0M5A34J0R3N5FM2CMMMAZ6',
                  'SPAXYA5XS51713FDTQ8H94EJ4V579CXMTRNBZKSF', #clarity example
                #transient's address

                  'S1G2081040G2081040G2081040G208105NK8PE5'
                   ]


class ExcludeHardcodedPrincipals(Visitor):
    MSG = "It is not recommended to hardcode known principals."

    def __init__(self):
        super().__init__()
        self.principal = ""

    def visit_node(self, node: Node, i):
        if i > 1:
            return
        
        self.principal = str(node.text, "utf-8")

        if self.principal in known_principals:
            pretty_print_warn(
                self,
                node.parent,
                node,
                self.MSG,
                None
            )