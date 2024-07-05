import sys
from dataclasses import dataclass
from typing import Optional

import tree_sitter_clarity
from tree_sitter import Language, TreeCursor, Parser, Tree, Node

__CLARITY__ = Language(tree_sitter_clarity.language())
__TIMES__ = 3

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

    def __init__(self, print_output: bool):
        self.source = self.src_name = None
        self.findings = []
        self.print_output = print_output

    def add_source(self, src: str, src_name: str = None):
        self.source = src
        self.src_name = src_name

    # noinspection PyShadowingBuiltins
    def visit_node(self, node: Node, round: int):
        sys.exit("visit_node not implemented")

    def get_contract_code_lines(self):
        return self.source.split('\n')

    def add_finding(self, node: Node, specific_node: Node):

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

    @classmethod
    @property
    def Name(cls):
        return cls.__name__


class NodeIterator:
    root_node: Node
    cursor: TreeCursor
    visited = []

    def __init__(self, node: Node):
        self.root_node = node
        self.cursor = node.walk()
        self.visited = []

        while self.cursor.goto_first_child():
            pass

    def next(self) -> Node | None:
        while True:
            node = self.node()

            if node not in self.visited:
                if self.cursor.goto_first_child():
                    continue
                self.visited.append(node)
                return node

            if self.cursor.goto_next_sibling():
                while self.cursor.goto_first_child():
                    pass
            else:

                if not self.cursor.goto_parent():
                    return None
                parent_node = self.cursor.node
                self.visited.append(parent_node)
                return parent_node

    def node(self) -> Node | None:
        return self.cursor.node

    def __iter__(self):
        return self

    def __next__(self) -> Node | None:
        node = self.next()
        if node is None:
            raise StopIteration
        return node


class LinterRunner:
    source: str
    tree: Tree
    root_node: Node
    iterator: NodeIterator
    lints: []  # lo que vaya acá adentro REQUIERE tener el metodo visit_node (at least) # XXX Happens to be a visitor=)
    round_number: int


    def __init__(self, source: str, print_output: bool, src_name: str):
        self.src_name = src_name
        self.source = source
        parser = Parser(__CLARITY__)
        self.tree = parser.parse(bytes(self.source, "utf8"))
        self.root_node = self.tree.root_node
        self.iterator = NodeIterator(self.root_node)
        self.lints = []
        self.round_number = 0
        self.print_output = print_output

    def run_lints(self, node: Node):
        for lint in self.lints:
            lint.visit_node(node, self.round_number)

    def add_lint(self, lint):
        self.lints.append(lint)
        return self

    def add_lints(self, lint_classes: [Visitor]):
        for lint_class in lint_classes:
            lint = lint_class(self.print_output)
            lint.add_source(self.source, self.src_name)
            self.lints.append(lint)

    def reset_cursor(self):
        self.iterator = NodeIterator(self.root_node)

    def run(self):
        for i in range(__TIMES__):
            self.round_number = self.round_number + 1
            while True:
                v = self.iterator.next()
                if v is None:
                    break
                self.run_lints(v)
            self.reset_cursor()

        return [finding for lint in self.lints
                for finding in lint.get_findings()]
