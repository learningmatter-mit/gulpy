import unittest as ut

from pymatgen.core import Structure

from gulpy.structure import GulpCrystal
from gulpy.structure.labels import CatlowLabels
from gulpy.tests.test_files import load_structure, load_molecule


class TestCatlow(ut.TestCase):
    def setUp(self):
        self.struct = load_structure()
        self.gcrys = GulpCrystal(self.struct, CatlowLabels())

    def test_labels(self):
        labels = [
            "Si",
            "Si",
            "Si",
            "Si",
            "Si",
            "Si",
            "Si",
            "Si",
            "O_O2-",
            "O_O2-",
            "O_O2-",
            "O_O2-",
            "O_O2-",
            "O_O2-",
            "O_O2-",
            "O_O2-",
            "O_O2-",
            "O_O2-",
            "O_O2-",
            "O_O2-",
            "O_O2-",
            "O_O2-",
            "O_O2-",
            "O_O2-",
        ]
        self.assertEqual(self.gcrys.get_labels(), labels)


if __name__ == "__main__":
    ut.main()
