import tree_sitter_clarity
from tree_sitter import Language, TreeCursor, Parser, Tree, Node

__CLARITY__ = Language(tree_sitter_clarity.language())
__TIMES__ = 3


class Visitor:
    source: str | None

    def __init__(self):
        self.source = None

    def add_source(self, source: str):
        self.source = source

    def visit_node(self, node: Node, i: int):
        pass


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
    lints: []  # lo que vaya acá adentro REQUIERE tener el metodo visit_node (at least)
    round_number: int

    def __init__(self, source: str):
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
            lint.add_source(self.source)
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
