import unittest as ut

from gulpy.jobs import MDJob
from gulpy.inputs.tests.test_library import ExampleLibrary
from gulpy.structure import GulpCrystal, GulpMolecule
from gulpy.structure.labels import CatlowLabels, DreidingMoleculeLabels
from gulpy.tests.test_files import load_structure, load_molecule, get_jobs_path


class TestJob(ut.TestCase):
    def setUp(self):
        self.structure = GulpCrystal(load_structure(), CatlowLabels())
        self.library = ExampleLibrary()

        self.job = MDJob(self.structure, self.library)

    def test_parse(self):
        results = self.job.parse_results(
            get_jobs_path("md/md.out"), get_jobs_path("md/md.trg")
        )

        self.assertTrue('frames' in results)


class TestMoleculeMDJob(ut.TestCase):
    def setUp(self):
        self.structure = GulpMolecule(load_molecule(), DreidingMoleculeLabels())
        self.library = ExampleLibrary()

        self.job = MDJob(self.structure, self.library)

    def test_parse(self):
        results = self.job.parse_results(
            get_jobs_path("md/molecule.out"), get_jobs_path("md/molecule.trg")
        )

        self.assertTrue('frames' in results)


if __name__ == "__main__":
    ut.main()
