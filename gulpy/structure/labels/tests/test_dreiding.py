import os
import unittest as ut

from pymatgen.core import Molecule
from gulpy.structure import GulpMolecule
from gulpy.structure.labels import DreidingMoleculeLabels
from gulpy.tests.test_files import load_structure, load_molecule


class TestDreiding(ut.TestCase):
    def setUp(self):
        self.pmgmol = load_molecule()
        self.smiles = 'CC'
        self.gmol = GulpMolecule.from_smiles(
            self.pmgmol.cart_coords,
            self.smiles,
            labels=DreidingMoleculeLabels()
        )

    def test_labels(self):
        self.assertEqual(self.gmol.get_labels(), ['C_3'] * 2 + ['H_'] * 6)


if __name__ == "__main__":
    ut.main()

