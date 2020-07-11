import unittest as ut

from gulpy.jobs import OptiJob
from gulpy.inputs.tests.test_library import ExampleLibrary
from gulpy.structure import GulpCrystal
from gulpy.structure.labels import DreidingLabels
from gulpy.tests.test_files import load_structure, get_jobs_path


class TestJob(ut.TestCase):
    def setUp(self):
        self.job = OptiJob(None, None)

    def test_parse(self):
        results = self.job.parse_results(get_jobs_path("opti/opti.out"))

        self.assertAlmostEqual(results["gnorm"], 0.06196731)
        self.assertAlmostEqual(results["energy"], 64.96556639)
        self.assertAlmostEqual(results["duration"], 22.8976)
        self.assertEqual(results["version"], "5.1.1")


if __name__ == "__main__":
    ut.main()
