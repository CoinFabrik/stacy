import math
import sys

from tree_sitter import Node

from .visitor import Visitor

tty = sys.stdout.isatty()


class TerminalColors:
    HEADER = '\033[95m' if tty else ''
    OKCYAN = '\033[96m' if tty else ''
    ENDC = '\033[0m' if tty else ''


def pretty_print_warn(visitor: Visitor, parent: Node, specific_node: Node, msg: str, help_msg: str | None,
                      footnote: str | None):
    line_number = parent.start_point.row + 1
    num_size_spaces = " " * (int(math.log10(line_number)) + 2)
    contract_code = visitor.source.split('\n')[line_number - 1]
    start_tabs = contract_code.count('\t') + 1
    contract_code = contract_code.replace('\t', '    ')

    arrows = "^" * (specific_node.end_point.column - specific_node.start_point.column)
    spaces = " " * ((specific_node.start_point.column * start_tabs) + 1)

    print(f"{TerminalColors.OKCYAN}Warning:{TerminalColors.ENDC} {msg}")

    print(f" {num_size_spaces}|")
    print(f" {line_number} | {contract_code}")
    print(f" {num_size_spaces}|{spaces}{TerminalColors.OKCYAN}{arrows}{TerminalColors.ENDC}")
    if help_msg is not None:
        print(f" {num_size_spaces}|{spaces}{help_msg}")
    if footnote is not None:
        print(f" {num_size_spaces}{TerminalColors.OKCYAN}Note: {TerminalColors.ENDC}{footnote}")

    print()
