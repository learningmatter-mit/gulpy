import os
import unittest as ut

from pymatgen.core import Molecule
from gulpy.structure import GulpMolecule


class TestGulpMolecule(ut.TestCase):
    def setUp(self):
        self.pmgmol = Molecule.from_file('ethane.xyz')
        self.smiles = 'CC'
        self.gmol = GulpMolecule.from_smiles(self.pmgmol.cart_coords, self.smiles)

    def test_labels(self):
        self.assertEqual(self.gmol.get_labels(), ['C'] * 2 + ['H'] * 6)

    def test_bonds(self):
        bonds = [(0, 1, 'single'), (0, 2, 'single'), (0, 3, 'single'), (0, 4, 'single'), (1, 5, 'single'), (1, 6, 'single'), (1, 7, 'single')]
        self.assertEqual(self.gmol.get_bonds(), bonds)


if __name__ == "__main__":
    ut.main()
