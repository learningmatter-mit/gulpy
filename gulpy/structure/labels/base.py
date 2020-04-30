class Labels:
    def __call__(self, symbol):
        return symbol


class MoleculeLabels(Labels):
    def is_hydrogen(self, atom):
        return atom.GetSymbol() == 'H'

    def get_hybridization(self, atom):
        hyb = str(atom.GetHybridization())
        hyb = hyb.strip('SP')
        hyb = '1' if hyb == '' else hyb

        assert hyb in ['1', '2', '3'], \
            'No hybridization assigned for the atom!'

        return hyb

    def __call__(self, atom):
        """Gets the label for the given atom"""
        return atom.GetSymbol()

