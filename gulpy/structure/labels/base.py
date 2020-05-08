from rdkit.Chem import Mol, Atom
from pymatgen.core import Structure


class Labels:
    def get_labels(self, structure: Structure) -> list:
        return [
            site.species_string
            for site in structure.sites
        ]

    def has_shell(self, structure: Structure) -> list:
        return [
            False
            for site in structure.sites
        ]


class MoleculeLabels:
    def is_hydrogen(self, atom: Atom):
        return atom.GetSymbol() == 'H'

    def get_hybridization(self, atom: Atom):
        hyb = str(atom.GetHybridization())
        hyb = hyb.strip('SP')
        hyb = '1' if hyb == '' else hyb

        assert hyb in ['1', '2', '3'], \
            'No hybridization assigned for the atom!'

        return hyb

    def get_labels(self, mol) -> list:
        return [
            atom.GetSymbol()
            for atom in mol.GetAtoms()
        ]

    def has_shell(self) -> list:
        return [
            False
            for atom in self.mol.GetAtoms()
        ]
