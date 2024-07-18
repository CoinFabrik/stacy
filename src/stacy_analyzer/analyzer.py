import argparse
import inspect
import os
import sys
from importlib.util import spec_from_file_location, module_from_spec

from stacy_analyzer.linter_runner import LinterRunner
from stacy_analyzer.print_message import TerminalColors
from stacy_analyzer.visitor import Visitor, Finding


class Analyzer:
    DETECTOR_MAP = {}

    @staticmethod
    def find_detectors():
        found = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        detectors_dir = os.path.join(current_dir, 'detectors')

        for fname in os.listdir(detectors_dir):
            if not fname.endswith('.py') or fname == '__init__.py':
                continue

            module_name = fname[:-3]
            module_path = os.path.join(detectors_dir, fname)

            spec = spec_from_file_location(module_name, module_path)
            mod = module_from_spec(spec)
            spec.loader.exec_module(mod)

            for attr in dir(mod):
                if attr == 'Visitor':
                    continue
                obj = getattr(mod, attr)
                if inspect.isclass(obj) and issubclass(obj, Visitor):
                    found.append(obj)

        return {obj.__name__: obj for obj in found}

    def __init__(self):
        self.DETECTOR_MAP = self.find_detectors()
        self.isatty = sys.stdout.isatty()

    def main(self):
        arg_parser = argparse.ArgumentParser(description='Static Analyzer for the Clarity language from Stacks')
        subparsers = arg_parser.add_subparsers(dest="command", help="Commands")

        lint_parser = subparsers.add_parser("lint", help="Run detectors in a given contract or contracts directory")
        lint_parser.add_argument("path", type=str, help="Path")
        lint_parser.add_argument("--filter", nargs="+", type=str, help="Comma-separated list of detector names to use")
        lint_parser.add_argument("--exclude", nargs="+", type=str,
                                 help="Comma-separated list of detector names to exclude")
        list_detectors = subparsers.add_parser("detectors", help="List detectors")
        lint_parser.add_argument("-A", nargs="+", type=int,
                                 help="Print A lines of trailing context after findings.")
        lint_parser.add_argument("-B", nargs="+", type=int,
                                 help="Print B lines of leading context before findings.")
        lint_parser.add_argument("-C", nargs="+", type=int,
                                 help="Print C lines of leading and trailing context after and before findings. Takes precedence over -A and -B")
        user_args = arg_parser.parse_args()
        if user_args.command == "lint":

            tc = 0
            lc = 0

            if user_args.A is not None:
                tc = user_args.A[0]

            if user_args.B is not None:
                lc = user_args.B[0]

            if user_args.C is not None:
                tc = user_args.C[0]
                lc = user_args.C[0]

            filters = list(self.DETECTOR_MAP.keys()) if user_args.filter is None else user_args.filter[0].split(',')
            excludes = [] if user_args.exclude is None else user_args.exclude[0].split(',')
            detectors = self.get_detectors(filters, excludes)
            path = user_args.path
            if path.endswith(".clar"):
                self.lint_file(path, detectors, True, lc, tc)
            else:
                for root, _, files in os.walk(path):
                    for file in files:
                        if file.endswith(".clar"):
                            self.lint_file(os.path.join(root, file), detectors, True, lc, tc)

        if user_args.command == "detectors":
            convert_camel_case = lambda s: s[0] + ''.join(' ' + c if c.isupper() else c for c in s[1:])
            detectors = list(map(convert_camel_case, self.DETECTOR_MAP.keys()))

            max_length = max(len(st) for st in detectors)
            s = max_length // 2 - 4

            if self.isatty:
                color = TerminalColors.OKCYAN
                end = TerminalColors.ENDC
            else:
                color = ""
                end = ""
            print(f" {color}┌" + "─" * s + " Detectors " + "─" * s + f"┐{end}")
            for file in detectors:
                print(
                    f" {color}|{end} {file.ljust(max_length + 1)}{color}|{end}")
            print(f" {color}└" + "─" * (max_length + 2) + f"┘{end}")

    def get_detectors(self, filters: str, excludes: str):
        all_detectors = set(self.DETECTOR_MAP.keys())
        filtered_names = set()
        for fil in filters:
            if fil not in all_detectors:
                print(f"{fil} is not a detector to filter.", file=sys.stderr)
            else:
                filtered_names.add(fil)

        for exc in excludes:
            if exc not in all_detectors:
                print(f"{exc} is not a detector to exclude.", file=sys.stderr)
            if exc in filtered_names:
                filtered_names.remove(exc)

        return [self.DETECTOR_MAP[name] for name in filtered_names]

    def lint_file(self, filename, lints: [Visitor], print_output: bool, leading: int, trailing: int):

        if print_output:
            if self.isatty:
                print(f"{TerminalColors.HEADER}====== Linting {filename}... ======{TerminalColors.ENDC}")
            else:
                print(f"====== Linting {filename}... ======")
        with open(filename, 'r') as file:
            source = file.read()

        runner: LinterRunner = LinterRunner(source, print_output, filename)
        runner.add_lints(lints, leading, trailing)

        findings: [Finding] = runner.run()

        return findings


if __name__ == '__main__':
    Analyzer().main()
