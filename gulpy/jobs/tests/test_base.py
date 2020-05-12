import unittest as ut

from gulpy.jobs import Job
from gulpy.inputs import Library
from gulpy.inputs.tests.test_library import ExampleLibrary
from gulpy.structure import GulpCrystal
from gulpy.structure.labels import CatlowLabels
from gulpy.tests.test_files import load_structure


class TestJob(ut.TestCase):
    def setUp(self):
        self.structure = GulpCrystal(load_structure(), CatlowLabels())
        self.library = ExampleLibrary()

        self.job = Job(self.structure, self.library)

    def test_keywords(self):
        self.assertEqual(self.job.keywords, [])

    def test_options(self):
        self.assertEqual(self.job.options, {})


if __name__ == "__main__":
    ut.main()
