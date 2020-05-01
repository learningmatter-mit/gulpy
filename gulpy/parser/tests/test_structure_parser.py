import unittest as ut

from gulpy.parser.single import StructureParser


class TestParser(ut.TestCase):
    def setUp(self):
        self.parser = StructureParser.from_file('opt_complex.out')

    def test_volume(self):
        vol = self.parser.get_volume()
        self.assertEqual(vol, 1328.491826)

    def test_num_atoms(self):
        n = self.parser.get_num_atoms()
        self.assertEqual(n, 130)

    def test_lattice(self):
        vectors = self.parser.get_lattice()
        expected = [[14.13378, -0.013675, 0.102028], [-0.01734, 17.029098, 0.00445], [0.038047, 0.001309, 4.992079]]
        self.assertEqual(vectors, expected)

    def test_input_lattice(self):
        vectors = self.parser.get_input_lattice()
        expected = [
            [14.110542, 0.0, 0.0],
            [0.0, 17.892402, 0.0],
            [0.0, 0.0, 5.261948]
        ]
        self.assertEqual(vectors, expected)

    def test_frac_coords(self):
        coords = self.parser.get_frac_coords()



if __name__ == "__main__":
    ut.main()
