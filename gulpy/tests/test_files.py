import os
import unittest as ut
from pymatgen.core import Structure, Molecule
from pymatgen.io.xyz import XYZ


thisdir = os.path.dirname(os.path.abspath(__file__))
inpath = os.path.join(thisdir, "files")


def load_structure(filename="ABW.cif"):
    path = os.path.join(inpath, filename)
    return Structure.from_file(path)


def load_molecule(filename="ethane.xyz"):
    path = os.path.join(inpath, filename)
    return Molecule.from_file(path)


class TestInputs(ut.TestCase):
    def setUp(self):
        self.structure = load_structure()
        self.molecule = load_molecule()

    def test_struct(self):
        self.assertEqual(len(self.structure), 24)

    def test_molecule(self):
        self.assertEqual(len(self.molecule), 8)


if __name__ == "__main__":
    ut.main()
