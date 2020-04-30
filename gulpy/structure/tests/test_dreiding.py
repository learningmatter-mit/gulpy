import os
import unittest as ut

from pymatgen.core import Molecule
from gulpy.structure import GulpMolecule
from gulpy.structure.labels import DreidingLabels


class TestDreiding(ut.TestCase):
    def setUp(self):
        self.pmgmol = Molecule.from_file('ethane.xyz')
        self.smiles = 'CC'
        self.gmol = GulpMolecule.from_smiles(
            self.pmgmol.cart_coords,
            self.smiles,
            labels=DreidingLabels()
        )

    def test_labels(self):
        self.assertEqual(self.gmol.get_labels(), ['C_3'] * 2 + ['H_'] * 6)


if __name__ == "__main__":
    ut.main()

