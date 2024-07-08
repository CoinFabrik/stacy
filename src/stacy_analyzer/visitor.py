import sys
from dataclasses import dataclass
from typing import Optional
from tree_sitter import Node

from stacy_analyzer.print_message import pretty_print_warn


@dataclass
class Location:
    lineno: int
    start_tabs: int
    span: tuple[int, int]
    line_code: str


@dataclass
class Finding:
    marked_nodes: (Node, Node)
    visitor: str
    source: str
    msg: str
    help_msg: Optional[str]
    footnote: Optional[str]
    location: Optional[Location]


class Visitor:
    source: str | None
    MSG: str
    HELP: str | None
    FOOTNOTE: str | None
    print_output: bool
    ignores: dict[str, ([int], Node)]

    def __init__(self, print_output: bool):
        self.ignores = {}
        self.source = self.src_name = None
        self.findings = []
        self.print_output = print_output

    def add_source(self, src: str, src_name: str = None):
        self.source = src
        self.src_name = src_name

    def set_ignores(self, ignores):
        self.ignores = ignores

    # noinspection PyShadowingBuiltins
    def visit_node(self, node: Node, round: int):
        sys.exit("visit_node not implemented")

    def get_contract_code_lines(self):
        return self.source.split('\n')

    def add_finding(self, node: Node, specific_node: Node):
        if self.finding_is_ignored(node):
            return

        if self.print_output:
            pretty_print_warn(self, node, specific_node, self.MSG, self.HELP, self.FOOTNOTE)

        parent = node.parent
        line_number = parent.start_point.row + 1
        line_code = self.get_contract_code_lines()[line_number - 1]
        location = Location(parent.start_point.row + 1,
                            line_code.count('\t') + 1,
                            (node.start_point.column, node.end_point.column),
                            self.get_contract_code_lines()[line_number - 1])
        finding = Finding((node, specific_node), self.Name, self.src_name, self.MSG, self.HELP, self.FOOTNOTE, location)
        self.findings.append(finding)
        return sorted(self.findings, key=lambda f: f.location.lineno)

    def get_findings(self):
        return self.findings

    def get_ignored_findings(self):
        return self.ignores

    def finding_is_ignored(self, node):
        line_node = node.start_point.row

        if self.Name in self.ignores and line_node in self.ignores[self.Name][0]:
            self.ignores[self.Name][0].remove(line_node)
            return True

        return False

    @property
    def Name(self):
        return self.__class__.__name__

