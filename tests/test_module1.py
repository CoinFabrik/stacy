import os
import time
import unittest

from stacy_analyzer.analyzer import Analyzer

__DETECTOR_QUANTITY__ = 11


class TestFind1Detector(unittest.TestCase):
    def test_add(self):
        a = Analyzer()
        self.assertTrue(len(a.DETECTOR_MAP) == __DETECTOR_QUANTITY__, f"{a.DETECTOR_MAP}")
        print("Detector count is OK")

    def test_detector_file(self):
        p = '.'
        for root, dirs, files in os.walk(p):
            for name in files:
                if not name.endswith('.clar') or name == "magic_comment.clar":
                    continue
                filename = os.path.join(root, name)
                a = Analyzer()
                for detector in a.DETECTOR_MAP.values():
                    a = Analyzer()
                    ret = a.lint_file(filename, [detector], False, 0, 0)
                    is_vulnerable_path = "vulnerable" in filename
                    is_correct_detector = detector.__name__.lower() in filename.replace('_', '')

                    expected = "at least one" if (is_vulnerable_path and is_correct_detector) else "zero"
                    actual = len(ret)

                    self.assertTrue(
                        (actual >= 1 if (is_vulnerable_path and is_correct_detector) else actual == 0),
                        f"Test failed for: {detector.__name__} @ {filename}. \n"
                        f"Expected {expected} lint(s), but found {actual}. \n"
                        f"Lints: {ret}\n"
                    )
        print("All detectors tests passed")

    def test_profile_time(self):
        filename = 'unused_arguments/vulnerable-example/unused_arguments.clar'
        a = Analyzer()
        lints = [detectorKlass for detectorKlass in a.DETECTOR_MAP.values()]
        start = time.time()
        for _ in range(1000):
            a = Analyzer()
            a.lint_file(filename, [detectorKlass for detectorKlass in lints], False, 0, 0)
        end = time.time()
        print(f'Running 1000 times in `unused_arguments` test case. Took: {end - start:f}s')


if __name__ == '__main__':
    unittest.main()
