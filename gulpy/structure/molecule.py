import re
import rdkit.Chem.AllChem as Chem
from rdkit.Chem import Mol, Conformer, MolFromSmiles

from .labels import Labels


DEFAULT_BONDS = {
    'SINGLE': 'single',
    'DOUBLE': 'double',
    'TRIPLE': 'triple',
    'AROMATIC': 'resonant'
}


class GulpMolecule:
    """Class to deal with labels of atoms for GULP.
        Analyzes the hybridization and the coordination 
        of each atom to assign the correct bonds.
    """

    def __init__(self, mol, labels=Labels()):
        self.mol = mol
        self.labels = labels

    @classmethod
    def from_smiles(cls, coords, smiles, add_hydrogens=True, labels=Labels()):
        mol = to_mol(coords, smiles, add_hydrogens)
        return cls(mol, labels=labels)

    def get_labels(self):
        return [
            self.labels(atom)
            for atom in self.mol.GetAtoms()
        ]

    def get_bonds(self):
        bonds = []
        for bond in self.mol.GetBonds():
            atom_1 = bond.GetBeginAtomIdx()
            atom_2 = bond.GetEndAtomIdx()
            btype = DEFAULT_BONDS[str(bond.GetBondType())]
            bonds.append((atom_1, atom_2, btype))

        return bonds
    

def to_mol(coords, smiles, add_hydrogens=True):
    mol = MolFromSmiles(smiles)
    if add_hydrogens:
        mol = Chem.AddHs(mol)

    conformer = Conformer(len(coords))
    for i, xyz in enumerate(coords):
        conformer.SetAtomPosition(i, xyz)
    
    mol.AddConformer(conformer)

    return mol


