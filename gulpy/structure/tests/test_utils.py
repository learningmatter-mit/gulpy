import unittest as ut

from pymatgen.core import Molecule
from gulpy.structure.utils import MoleculeExtractor
from gulpy.tests.test_files import load_molecule_structure


class TestExtractMolecule(ut.TestCase):
    def setUp(self):
        self.struct = load_molecule_structure()
        self.extractor = MoleculeExtractor(self.struct)

    def test_extraction(self):
        indices = list(range(len(self.struct)))
        extracted = self.extractor.extract_molecule(indices)

        self.assertEqual(len(extracted), 29)
