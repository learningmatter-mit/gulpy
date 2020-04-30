import re
from docking.zeolite.molecule import get_mol


ATOMS_WITH_HYBRIDIZATION = [
    'B', 'C', 'N', 'O', 'F', 'Cl', 'Br', 'I',
    'Al', 'Si', 'P', 'S', 'Ga', 'Ge', 'As', 'Se',
    'Sb', 'Te'
]


DEFAULT_LABELS = {
    'H': 'H_',
    'C': 'C_3',
    'O': 'O_3',
    'N': 'N_3',
    'Si': 'Si3',
    'Ge': 'Ge3',
    'Ga': 'Ga3',
}


DEFAULT_BONDS = {
    'SINGLE': 'single',
    'DOUBLE': 'double',
    'TRIPLE': 'triple',
    'AROMATIC': 'resonant'
}


class Molecule:
    """Class to deal with labels of atoms for the
        Dreiding potential. Analyzes the hybridization and
        the coordination of each atom to assign the correct
        values.
    """

    def __init__(self, smiles, xyz):
        self.mol = get_mol(smiles, xyz)

    @classmethod
    def from_geom(cls, geom):
        return cls(
            geom.species.smiles,
            geom.xyz
        )

    def get_labels(self):
        labels = []
        for atom in self.mol.GetAtoms():
            symbol = atom.GetSymbol()
            hybridization = self.get_atom_hybridization(atom)

            label = symbol + hybridization
            labels.append(label)

        return labels

    def get_bonds(self):
        bonds = []
        for bond in self.mol.GetBonds():
            atom_1 = bond.GetBeginAtomIdx()
            atom_2 = bond.GetEndAtomIdx()
            btype = DEFAULT_BONDS[str(bond.GetBondType())]
            bonds.append((atom_1, atom_2, btype))

        return bonds
    
    def get_atom_hybridization(self, atom):
        if self.is_hydrogen(atom):
            return self.get_hydrogen_hybridization(atom)

        if atom.GetIsAromatic():
            return '_R'

        if self.has_hybridization(atom):
            return self.get_hybridization_label(atom)
        else:
            return ''

    def is_hydrogen(self, atom):
        return atom.GetSymbol() == 'H'

    def get_hydrogen_hybridization(self, atom):
        if self.is_hydrogen_bonding(atom):
            return '___A'
        else:
            return '_'

    def is_hydrogen_bonding(self, atom):
        for nbr in atom.GetNeighbors():
            if nbr.GetSymbol() in ['N', 'O', 'S']:
                return True

        return False

    def get_hybridization_label(self, atom):
        hyb = str(atom.GetHybridization())
        hyb = hyb.strip('SP')
        hyb = '1' if hyb == '' else hyb

        assert hyb in ['1', '2', '3'], \
            'No hybridization assigned for the atom!'

        return '_%s' % hyb

    def has_hybridization(self, atom):
        symbol = atom.GetSymbol()
        return symbol in ATOMS_WITH_HYBRIDIZATION
