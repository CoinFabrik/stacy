import os
import argparse
import sys

from stacks_analyzer.detectors.VarCouldBeConstant import VarCouldBeConstant
from .detectors.TxSenderInAssert import TxSenderInAssert
from .detectors.AssertBlockHeight import AssertBlockHeight
from .detectors.DivideBeforeMultiply import DivideBeforeMultiply
from .detectors.PrivateFunctionNotUsed import PrivateFunctionNotUsed
from .detectors.UnwrapPanicUsage import UnwrapPanicUsage
from .detectors.CallInsideAsContract import CallInsideAsContract
from .detectors.UpdatedFunctionsDetector import UpdatedFunctionsDetector

from .print_message import TerminalColors

from .visitor import LinterRunner, Visitor

DETECTOR_MAP = {
    "AssertBlockHeight": AssertBlockHeight(),
    "CallInsideAsContract": CallInsideAsContract(),
    "DivideBeforeMultiply": DivideBeforeMultiply(),
    "PrivateFunctionNotUsed": PrivateFunctionNotUsed(),
    "TxSenderInAssert": TxSenderInAssert(),
    "UnwrapPanicUsage": UnwrapPanicUsage(),
    "VarCouldBeConstant": VarCouldBeConstant(),
    "UpdatedFunctionsDetector": UpdatedFunctionsDetector(),
}


def main():
    arg_parser = argparse.ArgumentParser(description='Static Analyzer for the Clarity language from Stacks')
    subparsers = arg_parser.add_subparsers(dest="command", help="Commands")

    lint_parser = subparsers.add_parser("lint", help="Run detectors in a given contract or contracts directory")
    lint_parser.add_argument("path", type=str, help="Path")
    lint_parser.add_argument("--filter", nargs="+", type=str, help="Comma-separated list of detector names to use")
    lint_parser.add_argument("--exclude", nargs="+", type=str, help="Comma-separated list of detector names to exclude")
    list_detectors = subparsers.add_parser("detectors", help="List detectors")

    args = arg_parser.parse_args()

    filters = args.filter or list(DETECTOR_MAP.keys())
    excludes = args.exclude or []
    detectors = get_detectors(filters, excludes)

    if args.command == "lint":
        path = args.path
        if path.endswith(".clar"):
            lint_file(path, detectors)
        else:
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".clar"):
                        lint_file(os.path.join(root, file), detectors)

    if args.command == "detectors":
        detectors = list(DETECTOR_MAP.keys())

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

def get_detectors(filters: str, excludes):
    all_detectors = list(DETECTOR_MAP.keys())
    if len(filters) != len(all_detectors):
        filters = filters[0].split(',')
    if excludes:
        excludes = excludes[0].split(',')
    filtered_names = []
    for fil in filters:
        if fil not in all_detectors:
            print(f"{fil} is not a detector to filter.", file=sys.stderr)
        else:
            filtered_names.append(fil)

    for exc in excludes:
        if exc not in all_detectors:
            print(f"{exc} is not a detector to exclude.", file=sys.stderr)
        if exc in filtered_names:
            filtered_names.remove(exc)

    detectors = []
    for name in filtered_names:
        detectors.append(DETECTOR_MAP[name])
    return detectors



def lint_file(path, lints: [Visitor]):
    tty = sys.stdout.isatty()
    if tty:
        print(f"{TerminalColors.HEADER}====== Linting {path}... ======{TerminalColors.ENDC}")

    else:
        print(f"====== Linting {path}... ======")

    with open(path, 'r') as file:
        source = file.read()

    runner: LinterRunner = LinterRunner(source)

    runner.add_lints(lints)
    runner.run()


if __name__ == '__main__':
    main()
