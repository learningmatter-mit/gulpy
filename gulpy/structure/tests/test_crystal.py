import unittest as ut

from pymatgen.core import Structure

from gulpy.structure import GulpCrystal
from gulpy.structure.labels import DreidingLabels


class TestGulpCrystal(ut.TestCase):
    def setUp(self):
        self.struct = Structure.from_file('ABW.cif')
        self.gcrys = GulpCrystal(self.struct, DreidingLabels())

    def test_labels(self):
        labels = ['Si3', 'Si3', 'Si3', 'Si3', 'Si3', 'Si3', 'Si3', 'Si3', 'O_3', 'O_3', 'O_3', 'O_3', 'O_3', 'O_3', 'O_3', 'O_3', 'O_3', 'O_3', 'O_3', 'O_3', 'O_3', 'O_3', 'O_3', 'O_3']
        self.assertEqual(self.gcrys.get_labels(), labels)

    def test_bonds(self):
        bonds = [(1, 13, 'single'), (1, 21, 'single'), (1, 17, 'single'), (1, 9, 'single'), (2, 14, 'single'), (2, 22, 'single'), (2, 18, 'single'), (2, 10, 'single'), (3, 9, 'single'), (3, 15, 'single'), (3, 23, 'single'), (3, 19, 'single'), (4, 10, 'single'), (4, 16, 'single'), (4, 24, 'single'), (4, 20, 'single'), (5, 11, 'single'), (5, 19, 'single'), (5, 15, 'single'), (5, 22, 'single'), (6, 12, 'single'), (6, 20, 'single'), (6, 16, 'single'), (6, 21, 'single'), (7, 17, 'single'), (7, 13, 'single'), (7, 24, 'single'), (7, 11, 'single'), (8, 18, 'single'), (8, 14, 'single'), (8, 23, 'single'), (8, 12, 'single')]
        self.assertEqual(self.gcrys.get_bonds(), bonds)


if __name__ == "__main__":
    ut.main()
