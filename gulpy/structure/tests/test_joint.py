import unittest as ut
import numpy as np

from pymatgen.core import Structure, Molecule

from gulpy.structure import JointStructure, GulpCrystal, GulpMolecule
from gulpy.structure.labels import DreidingLabels, DreidingMoleculeLabels
from gulpy.tests.test_files import load_structure, load_molecule


class TestJointStructure(ut.TestCase):
    def setUp(self):
        self.struct = load_structure()
        self.gcrys = GulpCrystal(self.struct, DreidingLabels())

        self.pmgmol = load_molecule()
        self.smiles = "CC"
        self.gmol = GulpMolecule.from_smiles(
            self.pmgmol.cart_coords, self.smiles, labels=DreidingMoleculeLabels()
        )

        self.joint = self.gcrys + self.gmol

    def test_add(self):
        self.assertIsInstance(self.joint, JointStructure)
        self.assertEqual(len(self.joint), len(self.gcrys) + len(self.gmol))

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
            "C_3",
            "C_3",
            "H_",
            "H_",
            "H_",
            "H_",
            "H_",
            "H_",
        ]
        self.assertEqual(self.joint.get_labels(), labels)

    def test_bonds(self):

        bonds_gcrys = [
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
        bonds_gmol = [
            (1, 2, "single"),
            (1, 3, "single"),
            (1, 4, "single"),
            (1, 5, "single"),
            (2, 6, "single"),
            (2, 7, "single"),
            (2, 8, "single"),
        ]
        bonds_gmol = [
            (u + len(self.gcrys), v + len(self.gcrys), btype)
            for u, v, btype in bonds_gmol
        ]

        self.assertEqual(self.joint.get_bonds(), bonds_gcrys + bonds_gmol)

    def test_lattice(self):
        expected = np.array([
            [9.873, 0, 0],
            [0, 5.254, 0],
            [0, 0, 8.77]
        ])
        self.assertIsNone(np.testing.assert_almost_equal(
            self.joint.get_lattice(), expected
        ))


if __name__ == "__main__":
    ut.main()
