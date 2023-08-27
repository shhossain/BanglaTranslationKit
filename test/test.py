import unittest
import sys
import os

# add ../ to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bntrans import Translator


def match_percentage(a, b):
    return len(set(a) & set(b)) / len(a)


class TestTranslator(unittest.TestCase):
    def test_translate(self):
        translator = Translator(src="en", dest="bn")

        tests = [
            ("Hello world!", "হ্যালো বিশ্ব!"),
            ("Who are you?", "তুমি কে?"),
            ("I am fine", "আমি ঠিক আছি"),
        ]

        for test in tests:
            # match percentage should be at least 70%
            result = match_percentage(translator.translate(test[0]), test[1])
            self.assertGreaterEqual(result, 0.5)

        translator = Translator(src="bn", dest="en")

        tests = [
            ("হ্যালো বিশ্ব!", "Hello world!"),
            ("তুমি কে?", "Who are you?"),
            ("আমি ঠিক আছি", "I am fine"),
        ]

        for test in tests:
            # match percentage should be at least 70%
            result = match_percentage(translator.translate(test[0]), test[1])
            self.assertGreaterEqual(result, 0.5)


if __name__ == "__main__":
    unittest.main()
