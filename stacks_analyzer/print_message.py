import math
import sys

from tree_sitter import Node

from .visitor import Visitor


class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def pretty_print_warn(visitor: Visitor, parent: Node, specific_node: Node, msg: str, help_msg: str | None):
    line_number = parent.start_point.row + 1
    num_size_spaces = " " * (int(math.log10(line_number)) + 2)
    contract_code = visitor.source.split('\n')[line_number - 1]
    start_tabs = contract_code.count('\t') + 1
    contract_code = contract_code.replace('\t', '    ')

    arrows = "^" * (specific_node.end_point.column - specific_node.start_point.column)
    spaces = " " * ((specific_node.start_point.column * start_tabs) + 1)

    tty = sys.stdout.isatty()

    if tty:
        print(f"{TerminalColors.OKCYAN}Warning:{TerminalColors.ENDC} {msg}")
    else:
        print(f"Warning: {msg}")
    print(f" {num_size_spaces}|")
    print(f" {line_number} | {contract_code}")
    if tty:
        print(f" {num_size_spaces}|{spaces}{TerminalColors.OKCYAN}{arrows}{TerminalColors.ENDC}")
    else:
        print(f" {num_size_spaces}|{spaces}{arrows}")

    if help_msg is not None:
        print(f" {num_size_spaces}|{spaces}{help_msg}")
    print()

