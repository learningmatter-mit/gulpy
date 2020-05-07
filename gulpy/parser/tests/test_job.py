import numpy as np
import unittest as ut
from pymatgen.core import Structure

from gulpy.parser import JobParser


class TestParser(ut.TestCase):
    def setUp(self):
        self.parser = JobParser.from_file("files/opti.out")

    def test_completed(self):
        self.assertTrue(self.parser.is_completed())

    def test_version(self):
        self.assertEqual(self.parser.get_version(), "5.1.1")

    def test_duration(self):
        self.assertEqual(self.parser.get_duration(), 22.8976)

    def test_nprocs(self):
        self.assertEqual(self.parser.get_nprocs(), 1)


if __name__ == "__main__":
    ut.main()
