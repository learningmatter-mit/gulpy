import os
import re
import numpy as np
import unittest as ut
from pymatgen.core import Structure


from gulpy.parser.base import Parser, FLOAT_REGEX, INT_REGEX


class TestRegex(ut.TestCase):
    def test_float(self):
        line = "4.15239802944899         0.333959824476882E-01      2.65878108583118"
        expected = [4.15239802944899, 0.333959824476882e-01, 2.65878108583118]
        matches = re.findall(FLOAT_REGEX, line)
        numbers = [float(x) for x in matches]

        for x, y in zip(numbers, expected):
            self.assertAlmostEqual(x, y)

    def test_int(self):
        line = "42 1e3    1E03"
        expected = [42, 1000, 1000]
        numbers = [float(x) for x in re.findall(INT_REGEX, line)]

        for x, y in zip(numbers, expected):
            self.assertAlmostEqual(x, y)


if __name__ == "__main__":
    ut.main()
