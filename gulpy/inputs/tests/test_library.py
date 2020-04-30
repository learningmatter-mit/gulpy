import os
import unittest as ut

from gulpy.inputs import Library


EXAMPLE_LIB = """species
Si    core  4.00000
O_O2- core  0.86902
O_O2- shel -2.86902
buckingham
Si core    O_O2- shel  1283.907 0.32052 10.66158 0.0 10.0
O_O2- shel O_O2- shel 22764.000 0.14900 27.87900 0.0 12.0
spring
O_O2-  74.92
three
Si core O_O2- shel O_O2- shel 2.09724 109.47 1.9 1.9 3.5"""


class TestBaseLibrary(ut.TestCase):
    def setUp(self):
        self.library = Library(EXAMPLE_LIB.split('\n'))

    def test_lines(self):
        species = {'O_O2-'}

        lib = self.library.get_lines_with_species(species)
        result = ['species', 'O_O2- core  0.86902', 'O_O2- shel -2.86902', 'buckingham', 'O_O2- shel O_O2- shel 22764.000 0.14900 27.87900 0.0 12.0', 'spring', 'O_O2-  74.92', 'three']
        self.assertEqual(lib, result)

    def test_get_library(self):
        species = {'Si'}
        lib = self.library.get_library(species)
        self.assertEqual(lib, ['species', 'Si    core  4.00000'])

    def test_get_library_two_elements(self):
        species = {'Si', 'O_O2-'}
        lib = self.library.get_library(species)
        cleaned_lib = ['species', 'Si    core  4.00000', 'O_O2- core  0.86902', 'O_O2- shel -2.86902', 'buckingham', 'Si core    O_O2- shel  1283.907 0.32052 10.66158 0.0 10.0', 'O_O2- shel O_O2- shel 22764.000 0.14900 27.87900 0.0 12.0', 'spring', 'O_O2-  74.92', 'three', 'Si core O_O2- shel O_O2- shel 2.09724 109.47 1.9 1.9 3.5']
        self.assertEqual(lib, cleaned_lib)

    def test_str(self):
        libstr = 'species\nSi    core  4.00000\nO_O2- core  0.86902\nO_O2- shel -2.86902\nbuckingham\nSi core    O_O2- shel  1283.907 0.32052 10.66158 0.0 10.0\nO_O2- shel O_O2- shel 22764.000 0.14900 27.87900 0.0 12.0\nspring\nO_O2-  74.92\nthree\nSi core O_O2- shel O_O2- shel 2.09724 109.47 1.9 1.9 3.5'

        self.assertEqual(str(self.library), libstr)

if __name__ == "__main__":
    ut.main()
