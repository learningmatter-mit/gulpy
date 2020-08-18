import os
import unittest as ut
from pymatgen.core import Structure, Molecule, Lattice
from pymatgen.io.xyz import XYZ


thisdir = os.path.dirname(os.path.abspath(__file__))
STRUCTURES = os.path.join(thisdir, "structures")
JOBS = os.path.join(thisdir, "jobs")


def get_jobs_path(filename):
    return os.path.join(JOBS, filename)


def load_structure(filename="ABW.cif"):
    path = os.path.join(STRUCTURES, filename)
    return Structure.from_file(path)


def load_molecule(filename="ethane.xyz"):
    path = os.path.join(STRUCTURES, filename)
    return Molecule.from_file(path)


def load_molecule_structure():
    frac_coords = [
        [0.726519, 0.201998, 0.016235],
        [0.775561, 0.250288, 0.064178],
        [0.832526, 0.167475, 0.099370],
        [0.918099, 0.101210, 0.069812],
        [0.000739, 0.168940, 0.041705],
        [0.889961, 0.229669, 0.142974],
        [0.814331, 0.288193, 0.179060],
        [0.746484, 0.088734, 0.120518],
        [0.788525, 0.010777, 0.160482],
        [0.663668, 0.143668, 0.024956],
        [0.786126, 0.163662, 0.991722],
        [0.689009, 0.265892, 0.993749],
        [0.711951, 0.288002, 0.086680],
        [0.834448, 0.312093, 0.054333],
        [0.875310, 0.048715, 0.043226],
        [0.959446, 0.050619, 0.097701],
        [0.048267, 0.218407, 0.067667],
        [0.056960, 0.115868, 0.021837],
        [0.964699, 0.220910, 0.012857],
        [0.943334, 0.288263, 0.125005],
        [0.939537, 0.172011, 0.163884],
        [0.767475, 0.349964, 0.159581],
        [0.759199, 0.233972, 0.198677],
        [0.861487, 0.328887, 0.208539],
        [0.680818, 0.137077, 0.136038],
        [0.715376, 0.043017, 0.088095],
        [0.722655, 0.959258, 0.173358],
        [0.850704, 0.957870, 0.145277],
        [0.820082, 0.051357, 0.194224],
    ]
    species = [
        "C",
        "C",
        "N",
        "C",
        "C",
        "C",
        "C",
        "C",
        "C",
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
    ]
    lattice = Lattice.from_parameters(
        12.46433002, 12.46420102, 26.22526509, 89.99366812, 90.00714732, 90.00004617
    )

    return Structure(coords=frac_coords, species=species, lattice=lattice)


class TestInputs(ut.TestCase):
    def setUp(self):
        self.structure = load_structure()
        self.molecule = load_molecule()
        self.molecule_structure = load_molecule_structure()

    def test_struct(self):
        self.assertEqual(len(self.structure), 24)

    def test_molecule(self):
        self.assertEqual(len(self.molecule), 8)

    def test_molecule_structure(self):
        self.assertEqual(len(self.molecule_structure), 29)


if __name__ == "__main__":
    ut.main()
