import os
import argparse
import sys

from stacks_analyzer.detectors.VarCouldBeConstant import VarCouldBeConstant
from .detectors.TxSenderInAssert import TxSenderDetector
from .detectors.AssertBlockHeight import AssertBlockHeightDetector
from .detectors.DivideBeforeMultiply import DivideBeforeMultiplyDetector
from .detectors.PrivateFunctionNotUsed import PrivateFunctionNotUsed
from .detectors.UnwrapPanicUsage import UnwrapPanicDetector
from .detectors.CallInsideAsContract import CallInsideAsContract
from .print_message import TerminalColors

from .visitor import LinterRunner, Visitor


def main():
    arg_parser = argparse.ArgumentParser(description='Static Analyzer for the Clarity language from Stacks')
    subparsers = arg_parser.add_subparsers(dest="command", help="Commands")

    lint_parser = subparsers.add_parser("lint", help="Run detectors in a given contract or contracts directory")
    lint_parser.add_argument("path", type=str, help="Path")
    list_detectors = subparsers.add_parser("detectors", help="List detectors")

    args = arg_parser.parse_args()

    if args.command == "lint":
        path = args.path
        if path.endswith(".clar"):
            lint_file(path)
        else:
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".clar"):
                        lint_file(os.path.join(root, file))

    if args.command == "detectors":
        detectors = [
            "AssertBlockHeight",
            "CallInsideAsContract",
            "DivideBeforeMultiply",
            "PrivateFunctionNotUsed",
            "TxSenderInAssert",
            "UnwrapPanicUsage",
            "VarCouldBeConstant"
        ]

        max_length = max(len(st) for st in detectors)
        s = max_length // 2 - 4

        if sys.stdout.isatty():
            color = TerminalColors.OKCYAN
            end = TerminalColors.ENDC
        else:
            color = ""
            end = ""

        if sys.stdout.isatty():
            print(f" {color}┌" + "─" * (s - 1) + " Detectors " + "─" * s + f"┐{end}")
            for file in detectors:
                print(
                    f" {color}|{end} {file.ljust(max_length + 1)}{color}|{end}")
            print(f" {color}└" + "─" * (max_length + 2) + f"┘{end}")



def lint_file(path):
    tty = sys.stdout.isatty()
    if tty:
        print(f"{TerminalColors.HEADER}====== Linting {path}... ======{TerminalColors.ENDC}")
        
    else:
        print(f"====== Linting {path}... ======")

    with open(path, 'r') as file:
        source = file.read()

    runner: LinterRunner = LinterRunner(source)

    lints: [Visitor] = [
        TxSenderDetector(),
        DivideBeforeMultiplyDetector(),
        UnwrapPanicDetector(),
        AssertBlockHeightDetector(),
        CallInsideAsContract(),
        PrivateFunctionNotUsed(),
        VarCouldBeConstant()
    ]

    runner.add_lints(lints)
    runner.run()


def generate_base_for_tests(path):
    tty = sys.stdout.isatty()
    contract_name = ''.join(['base_tests/', os.path.basename(path[:-5]),'.txt'])

    sys.stdout = open(contract_name, "w", encoding='utf8')
    if tty:
        print(f"====== Linting {path}... ======")
            
    else:
        print(f"====== Linting {path}... ======")

    with open(path, 'r') as file:
        source = file.read()

    runner: LinterRunner = LinterRunner(source)

    lints: [Visitor] = [
        TxSenderDetector(),
        DivideBeforeMultiplyDetector(),
        UnwrapPanicDetector(),
        AssertBlockHeightDetector(),
        CallInsideAsContract(),
        PrivateFunctionNotUsed(),
        VarCouldBeConstant()
    ]

    runner.add_lints(lints)
    runner.run()

if __name__ == '__main__':
    main()
