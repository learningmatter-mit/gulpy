import numpy as np
import unittest as ut
from pymatgen.core import Structure

from gulpy.parser import ErrorParser, JobParser
from gulpy.tests.test_files import get_jobs_path


class TestParser(ut.TestCase):
    def test_has_error(self):
        parser = JobParser.from_file(get_jobs_path("error/mdtemp_error.out"))
        self.assertTrue(parser.has_error())


if __name__ == "__main__":
    ut.main()
