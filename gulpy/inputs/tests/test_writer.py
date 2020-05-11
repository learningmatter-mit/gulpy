import os
import unittest as ut

from gulpy.inputs import InputWriter
from gulpy.structure import GulpCrystal
from gulpy.structure.labels import CatlowLabels
from gulpy.tests.test_files import load_structure

from gulpy.inputs.tests.test_library import ExampleLibrary


class TestInputWriter(ut.TestCase):
    def setUp(self):
        self.keywords = ['opti', 'conv']
        self.options = {
            'maxstep': 150
        }
        self.structure = load_structure()
        self.gcrys = GulpCrystal(self.structure, CatlowLabels())

        self.writer = InputWriter(
            self.keywords,
            self.options,
            self.gcrys,
            ExampleLibrary()
        )

    def test_keywords(self):
        self.assertEqual(
            self.writer._render_keywords(),
            'opti conv'
        )

    def test_options(self):
        self.assertEqual(
            self.writer._render_options(),
            'maxstep 150'
        )

    def test_lattice(self):
        expected = '\nvectors\n9.8730000 0.0000000 0.0000000\n-0.0000000 5.2540000 0.0000000\n0.0000000 0.0000000 8.7700000 \n'
        self.assertEqual(self.writer._render_lattice(), expected)

    def test_coords(self):
        expected = 'cartesian\n   Si    3.38446    1.31350    3.51414\n   Si    8.32096    3.94050    7.89914\n   Si    6.48854    1.31350    3.51414\n   Si    1.55204    3.94050    7.89914\n   Si    6.48854    3.94050    5.25586\n   Si    1.55204    1.31350    0.87086\n   Si    3.38446    3.94050    5.25586\n   Si    8.32096    1.31350    0.87086\nO_O2-    4.93650    1.31350    3.08967\nO_O2-   -0.00000    3.94050    7.47467\nO_O2-    4.93650    3.94050    5.68033\nO_O2-   -0.00000    1.31350    1.29533\nO_O2-    3.06063    0.00000    4.38500\nO_O2-    7.99713    2.62700    0.00000\nO_O2-    6.81237    0.00000    4.38500\nO_O2-    1.87587    2.62700    0.00000\nO_O2-    3.06063    2.62700    4.38500\nO_O2-    7.99713    0.00000    0.00000\nO_O2-    6.81237    2.62700    4.38500\nO_O2-    1.87587    0.00000    0.00000\nO_O2-    2.46825    1.31350    2.19250\nO_O2-    7.40475    3.94050    6.57750\nO_O2-    7.40475    1.31350    2.19250\nO_O2-    2.46825    3.94050    6.57750\n'

        self.assertEqual(self.writer._render_coords(), expected)

    def test_bonds(self):
        expected = 'connect 1 13 single\nconnect 1 21 single\nconnect 1 17 single\nconnect 1 9 single\nconnect 2 14 single\nconnect 2 22 single\nconnect 2 18 single\nconnect 2 10 single\nconnect 3 9 single\nconnect 3 15 single\nconnect 3 23 single\nconnect 3 19 single\nconnect 4 10 single\nconnect 4 16 single\nconnect 4 24 single\nconnect 4 20 single\nconnect 5 11 single\nconnect 5 19 single\nconnect 5 15 single\nconnect 5 22 single\nconnect 6 12 single\nconnect 6 20 single\nconnect 6 16 single\nconnect 6 21 single\nconnect 7 17 single\nconnect 7 13 single\nconnect 7 24 single\nconnect 7 11 single\nconnect 8 18 single\nconnect 8 14 single\nconnect 8 23 single\nconnect 8 12 single'

        self.assertEqual(self.writer._render_bonds(), expected)


if __name__ == "__main__":
    ut.main()
