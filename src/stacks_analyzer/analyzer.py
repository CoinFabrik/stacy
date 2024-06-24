import argparse
import inspect
import os
import sys

from stacks_analyzer.print_message import TerminalColors
from stacks_analyzer.visitor import LinterRunner, Visitor


class Number(object):
    def __init__(self, n):
        self.value = n

    def val(self):
        return self.value

    def add(self, n2):
        self.value += n2.val()

    def __add__(self, n2):
        return self.__class__(self.value + n2.val())

    def __str__(self):
        return str(self.val())

    @classmethod
    def addall(cls, number_obj_iter):
        cls(sum(n.val() for n in number_obj_iter))


class Analyzer:
    DETECTOR_MAP = {}

    @staticmethod
    def find_detectors():
        found = []
        for fname in os.listdir('.'):
            if not fname.endswith('.py'):
                continue
            mod = __import__(fname.replace('.py', ''), globals(), locals(), ['*'])
            for attr in dir(mod):
                if attr=='Visitor': continue
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

        user_args = arg_parser.parse_args()
        if user_args.command == "lint":
            filters = user_args.filter or list(self.DETECTOR_MAP.keys())
            excludes = user_args.exclude or []
            detectors = self.get_detectors(filters, excludes)
            path = user_args.path
            if path.endswith(".clar"):
                self.lint_file(path, detectors)
            else:
                for root, _, files in os.walk(path):
                    for file in files:
                        if file.endswith(".clar"):
                            self.lint_file(os.path.join(root, file), detectors)

        if user_args.command == "detectors":
            detectors = list(self.DETECTOR_MAP.keys())

            max_length = max(len(st) for st in detectors)
            s = max_length // 2 - 4

            if self.isatty:
                color = TerminalColors.OKCYAN
                end = TerminalColors.ENDC
            else:
                color = ""
                end = ""
            print(f" {color}┌" + "─" * (s - 1) + " Detectors " + "─" * s + f"┐{end}")
            for file in detectors:
                print(
                    f" {color}|{end} {file.ljust(max_length + 1)}{color}|{end}")
            print(f" {color}└" + "─" * (max_length + 2) + f"┘{end}")

    def get_detectors(self, filters: str, excludes=()):
        all_detectors = list(self.DETECTOR_MAP.keys())      ## shouldn't be a list!!!
        if len(filters) != len(all_detectors):  ## ???
            filters = filters[0].split(',')
        if excludes:
            excludes = excludes[0].split(',')
        filtered_names = []                                 ## again..
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

        # detectors = []
        # for name in filtered_names:
        #     detectors.append(self.DETECTOR_MAP[name])
        # return detectors
        return [self.DETECTOR_MAP[name] for name in filtered_names]

    def lint_file(self, filename, lints: [Visitor]):
        if self.isatty:
            print(f"{TerminalColors.HEADER}====== Linting {filename}... ======{TerminalColors.ENDC}")
        else:
            print(f"====== Linting {filename}... ======")
        with open(filename, 'r') as file:
            source = file.read()

        runner: LinterRunner = LinterRunner(source, filename)
        runner.add_lints(lints)
        return runner.run()


if __name__ == '__main__':
    Analyzer().main()
