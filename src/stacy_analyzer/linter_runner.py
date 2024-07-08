import re

import tree_sitter_clarity
from stacy_analyzer.print_message import TerminalColors
from tree_sitter import Language, Tree, Node, Parser

__CLARITY__ = Language(tree_sitter_clarity.language())
__TIMES__ = 3

from stacy_analyzer.visitor import Visitor
from stacy_analyzer.node_iterator import NodeIterator


class LinterRunner:
    source: str
    tree: Tree
    root_node: Node
    iterator: NodeIterator
    lints: [Visitor]
    round_number: int
    allowed_lints: dict[str, ([int], Node)] = {}

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
        self.allowed_lints = {}

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
        self.pre_run_checks()
        for i in range(__TIMES__):
            self.round_number = self.round_number + 1

            for node in self.iterator:
                self.run_lints(node)
            self.reset_cursor()

        self.post_run_checks()

        return [finding for lint in self.lints
                for finding in lint.get_findings()]

    def pre_run_checks(self):
        for node in self.iterator:
            allowed: [AllowedComment] = check_comments(node)
            if not allowed:
                continue
            for allowed_comment in allowed:
                if allowed_comment.name not in self.allowed_lints:
                    self.allowed_lints[allowed_comment.name] = (
                        [allowed_comment.line_number], allowed_comment.comment_node)
                else:
                    self.allowed_lints[allowed_comment.name][0].append(allowed_comment.line_number)

        self.reset_cursor()
        for lint in self.lints:
            lint.set_ignores(self.allowed_lints)

    def post_run_checks(self):
        for lint in self.lints:
            findings: dict[str, ([int], Node)] = lint.get_ignored_findings()
            name = lint.Name
            if name not in self.allowed_lints or findings[name][0] == []:
                continue
            warn_magic_comment(findings[name][0], name)


class AllowedComment:
    name: str
    comment_node: Node
    line_number: int

    def __init__(self, finding: str, comment_node: Node):
        self.name = finding
        self.comment_node = comment_node
        self.line_number = comment_node.range.start_point.row + 1


def extract_detectors(comment_text: str) -> [str]:
    allow_comment = re.search(r'#\[allow\((.*?)\)]', comment_text)
    return allow_comment.group(1).split(',') if allow_comment else []


def check_comments(node) -> [AllowedComment]:
    if node.grammar_name != "comment":
        return []
    comment_text = node.text.decode("utf-8")
    detectors = extract_detectors(comment_text)

    return [AllowedComment(detector.strip(), node) for detector in detectors]


def warn_magic_comment(lines: [int], name: str):
    for line in lines:
        print(f"{TerminalColors.ERROR}[WARNING]{TerminalColors.ENDC} "
              f"Magic comment in line {line} for detector {TerminalColors.BOLD}{name}{TerminalColors.ENDC} is not used")
