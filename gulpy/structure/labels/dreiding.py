from rdkit.Chem import Mol, Atom
from pymatgen.core import Structure

from .base import Labels, MoleculeLabels


class DreidingLabels(Labels):
    DEFAULT_LABELS = {
        'H': 'H_',
        'B': 'B_3',
        'C': 'C_3',
        'N': 'N_3',
        'O': 'O_3',
        'F': 'F_',
        'Cl': 'Cl',
        'Br': 'Br',
        'I': 'I_',
        'Al': 'Al3',
        'Si': 'Si3',
        'P': 'P_3',
        'S': 'S_3',
        'Ga': 'Ga3',
        'Ge': 'Ge3',
        'As': 'As3',
        'Se': 'Se3',
        'In': 'In3',
        'Sb': 'Sb3',
        'Te': 'Te3',
        'Na': 'Na',
        'Ca': 'Ca',
        'Fe': 'Fe',
        'Zn': 'Zn',
        'Ti': 'Ti',
        'Tc': 'Tc',
        'Ru': 'Ru',
    }

    def get_labels(self, structure: Structure) -> list:
        return [
            self.DEFAULT_LABELS[site.species_string]
            for site in structure.sites
        ]


class DreidingMoleculeLabels(MoleculeLabels):
    ATOMS_WITH_HYBRIDIZATION = [
        'B', 'C', 'N', 'O', 'F', 'Cl', 'Br', 'I',
        'Al', 'Si', 'P', 'S', 'Ga', 'Ge', 'As', 'Se',
        'Sb', 'Te'
    ]

    def get_labels(self, mol: Mol):
        return [
            atom.GetSymbol() + self.get_atom_hybridization(atom)
            for atom in mol.GetAtoms()
        ]
        return symbol + hyb

    def get_atom_hybridization(self, atom: Atom):
        if self.is_hydrogen(atom):
            return self.get_hydrogen_hybridization(atom)

        if atom.GetIsAromatic():
            return '_R'

        if self.has_hybridization(atom):
            return '_%s' % self.get_hybridization(atom)

        return ''

    def get_hydrogen_hybridization(self, atom: Atom):
        if self.is_hydrogen_bonding(atom):
            return '___A'
        else:
            return '_'

    def is_hydrogen_bonding(self, atom: Atom):
        return any([
            nbr.GetSymbol() in ['N', 'O', 'S']
            for nbr in atom.GetNeighbors()
        ])

    def has_hybridization(self, atom: Atom):
        symbol = atom.GetSymbol()
        return symbol in self.ATOMS_WITH_HYBRIDIZATION
