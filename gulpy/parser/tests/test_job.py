import numpy as np
import unittest as ut
from pymatgen.core import Structure

from gulpy.parser import JobParser
from gulpy.tests.test_files import get_jobs_path


class TestParser(ut.TestCase):
    def setUp(self):
        self.parser = JobParser.from_file(get_jobs_path("opti/opti.out"))

    def test_error(self):
        self.assertFalse(self.parser.has_error())

    def test_completed(self):
        self.assertTrue(self.parser.is_completed())

    def test_version(self):
        self.assertEqual(self.parser.get_version(), "5.1.1")

    def test_duration(self):
        self.assertEqual(self.parser.get_duration(), 22.8976)

    def test_nprocs(self):
        self.assertEqual(self.parser.get_nprocs(), 1)

    def test_host(self):
        parser = JobParser.from_file(get_jobs_path("slc/coreshell.out"))
        host = parser.get_host()
        self.assertEqual(host, "node1034")
        self.assertIsNone(self.parser.get_host())


if __name__ == "__main__":
    ut.main()
