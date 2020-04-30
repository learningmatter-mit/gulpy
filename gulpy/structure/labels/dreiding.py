from .base import Labels


class DreidingLabels(Labels):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
