import unittest as ut

from pymatgen.core import Structure

from gulpy.structure import GulpCrystal
from gulpy.structure.labels import DreidingLabels, CatlowLabels
from gulpy.tests.test_files import load_structure, load_molecule


class TestGulpCrystal(ut.TestCase):
    def setUp(self):
        self.struct = load_structure()
        self.gcrys = GulpCrystal(self.struct, DreidingLabels())

    def test_labels(self):
        labels = [
            "Si3",
            "Si3",
            "Si3",
            "Si3",
            "Si3",
            "Si3",
            "Si3",
            "Si3",
            "O_3",
            "O_3",
            "O_3",
            "O_3",
            "O_3",
            "O_3",
            "O_3",
            "O_3",
            "O_3",
            "O_3",
            "O_3",
            "O_3",
            "O_3",
            "O_3",
            "O_3",
            "O_3",
        ]
        self.assertEqual(self.gcrys.get_labels(), labels)

    def test_bonds(self):
        bonds = [
            (1, 13, "single"),
            (1, 21, "single"),
            (1, 17, "single"),
            (1, 9, "single"),
            (2, 14, "single"),
            (2, 22, "single"),
            (2, 18, "single"),
            (2, 10, "single"),
            (3, 9, "single"),
            (3, 15, "single"),
            (3, 23, "single"),
            (3, 19, "single"),
            (4, 10, "single"),
            (4, 16, "single"),
            (4, 24, "single"),
            (4, 20, "single"),
            (5, 11, "single"),
            (5, 19, "single"),
            (5, 15, "single"),
            (5, 22, "single"),
            (6, 12, "single"),
            (6, 20, "single"),
            (6, 16, "single"),
            (6, 21, "single"),
            (7, 17, "single"),
            (7, 13, "single"),
            (7, 24, "single"),
            (7, 11, "single"),
            (8, 18, "single"),
            (8, 14, "single"),
            (8, 23, "single"),
            (8, 12, "single"),
        ]
        self.assertEqual(self.gcrys.get_bonds(), bonds)

    def test_labels_with_shell(self):
        gcrys = GulpCrystal(self.struct, CatlowLabels())

        exp_labels = ["Si"] * 8 + ["O_O2-"] * (16 * 2)
        exp_core_shell = ["core"] * 8 + ["core", "shell"] * 16
        labels, core_shell = gcrys.get_labels_with_shells()
        self.assertEqual(labels, exp_labels)
        self.assertEqual(core_shell, exp_core_shell)


if __name__ == "__main__":
    ut.main()
