from dataclasses import dataclass
from typing import Optional

import tree_sitter_clarity
from tree_sitter import Language, TreeCursor, Parser, Tree, Node

__CLARITY__ = Language(tree_sitter_clarity.language())
__TIMES__ = 3

# from mypkg.print_message import pretty_print_warn


@dataclass
class Location:
    lineno: int
    start_tabs: int
    span: tuple[int, int]
    line_code: str


@dataclass
class Finding:
    visitor: str
    source: str
    msg: str
    help_msg: Optional[str]
    footnote: Optional[str]
    location: Optional[Location]


class Visitor:
    source: str | None
    MSG: str

    def __init__(self):
        self.source = self.src_name = None
        self.findings = []

    def add_source(self, source: str, src_name: str=None):
        self.source = source
        self.src_name = src_name

    # noinspection PyShadowingBuiltins
    def visit_node(self, node: Node, round: int):
        pass

    def get_contract_code_lines(self):
        return self.source.split('\n')

    def add_finding(self, node: Node, help_msg=None, footnote=None):
        # pretty_print_warn(self, node.parent, node, self.MSG, footnote)
        # -----
        parent = node.parent
        line_number = parent.start_point.row + 1
        line_code = self.get_contract_code_lines()[line_number - 1]
        location = Location(parent.start_point.row + 1,
                            line_code.count('\t') + 1,
                            (node.start_point.column, node.end_point.column),
                            self.get_contract_code_lines()[line_number - 1])
        finding = Finding(self.Name, self.src_name, self.MSG, help_msg, footnote, location)
        self.findings.append(finding)
        return finding

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
        self.visited = set()  #[]

        while self.cursor.goto_first_child():
            pass

    def next(self) -> Node | None:
        while True:
            node = self.node()

            if not node in self.visited:  # self.visited.__contains__(node):
                if self.cursor.goto_first_child():
                    continue
                self.visited.add(node)
                return node
            if self.cursor.goto_next_sibling():
                while self.cursor.goto_first_child():
                    pass
            else:
                if not self.cursor.goto_parent():
                    return None
                parent_node = self.cursor.node
                self.visited.add(parent_node)
                return parent_node

    def node(self) -> Node | None:
        return self.cursor.node


class LinterRunner:
    source: str
    tree: Tree
    root_node: Node
    iterator: NodeIterator
    lints: []  # lo que vaya acá adentro REQUIERE tener el metodo visit_node (at least) # XXX Happens to be a visitor=)
    round_number: int

    def __init__(self, source: str, src_name: str=None):
        self.src_name = src_name
        self.source = source
        parser = Parser(__CLARITY__)
        self.tree = parser.parse(bytes(self.source, "utf8"))
        self.root_node = self.tree.root_node
        self.iterator = NodeIterator(self.root_node)
        self.lints = []
        self.round_number = 0

    def run_lints(self, node: Node):
        for lint in self.lints:
            lint.visit_node(node, self.round_number)

    def add_lint(self, lint):
        self.lints.append(lint)
        return self

    def add_lints(self, lints):
        for lint in lints:
            lint.add_source(self.source, self.src_name)
        self.lints.extend(lints)

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
