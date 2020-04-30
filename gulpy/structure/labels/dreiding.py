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

    def __call__(self, symbol):
        return self.DEFAULT_LABELS[symbol]


class DreidingMoleculeLabels(MoleculeLabels):
    ATOMS_WITH_HYBRIDIZATION = [
        'B', 'C', 'N', 'O', 'F', 'Cl', 'Br', 'I',
        'Al', 'Si', 'P', 'S', 'Ga', 'Ge', 'As', 'Se',
        'Sb', 'Te'
    ]

    def __call__(self, atom):
        symbol = atom.GetSymbol()
        hyb = self.get_atom_hybridization(atom)
        return symbol + hyb

    def get_atom_hybridization(self, atom):
        if self.is_hydrogen(atom):
            return self.get_hydrogen_hybridization(atom)

        if atom.GetIsAromatic():
            return '_R'

        if self.has_hybridization(atom):
            return '_%s' % self.get_hybridization(atom)

        return ''

    def get_hydrogen_hybridization(self, atom):
        if self.is_hydrogen_bonding(atom):
            return '___A'
        else:
            return '_'

    def is_hydrogen_bonding(self, atom):
        return any([
            nbr.GetSymbol() in ['N', 'O', 'S']
            for nbr in atom.GetNeighbors()
        ])

    def has_hybridization(self, atom):
        symbol = atom.GetSymbol()
        return symbol in self.ATOMS_WITH_HYBRIDIZATION
