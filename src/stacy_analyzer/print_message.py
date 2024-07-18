import math
import sys

from tree_sitter import Node

tty = sys.stdout.isatty()


class TerminalColors:
    HEADER = '\033[95m' if tty else ''
    OKCYAN = '\033[96m' if tty else ''
    ERROR = '\033[31;1;4m' if tty else ''
    BOLD = '\033[1m' if tty else ''
    GREY = '\033[38;5;248m' if tty else ''
    ENDC = '\033[0m' if tty else ''
    EXCYAN = ''



def pretty_print_warn(visitor, parent: Node, specific_node: Node, msg: str, help_msg: str | None,
                      footnote: str | None, leading_context: int, trailing_context: int):
    line_number = parent.start_point.row + 1
    num_size_spaces = " " * (int(math.log10(line_number)) + 2)

    all_lines = visitor.source.split('\n')
    total_lines = len(all_lines)

    start_line = max(0, line_number - leading_context - 1)
    end_line = min(total_lines, line_number + trailing_context)

    print(f"{TerminalColors.OKCYAN}Warning:{TerminalColors.ENDC} {msg}")
    print(f" {num_size_spaces}{TerminalColors.OKCYAN}|{TerminalColors.ENDC}")

    for i in range(start_line, end_line):
        current_line = i + 1
        contract_code = all_lines[i]
        start_tabs = contract_code.count('\t') + 1
        contract_code = contract_code.replace('\t', '    ')

        print(f" {TerminalColors.OKCYAN}{current_line} |{TerminalColors.ENDC} {contract_code}")

        if current_line == line_number:
            arrows = "^" * (specific_node.end_point.column - specific_node.start_point.column)
            spaces = " " * ((specific_node.start_point.column * start_tabs) + 1)
            print(f" {num_size_spaces}{TerminalColors.OKCYAN}|{TerminalColors.ENDC}{spaces}{TerminalColors.OKCYAN}{arrows}{TerminalColors.ENDC}")
            if help_msg is not None:
                print(f" {num_size_spaces}{TerminalColors.OKCYAN}|{TerminalColors.ENDC}{spaces}{help_msg}")

    if footnote is not None:
        print(f" {num_size_spaces}{TerminalColors.OKCYAN}Note: {TerminalColors.GREY}{footnote}{TerminalColors.ENDC}")

    print()
