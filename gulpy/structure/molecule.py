import re
import rdkit.Chem.AllChem as Chem
from rdkit.Chem import Mol, Conformer, MolFromSmiles

from .base import GulpObject
from .labels import MoleculeLabels


class GulpMolecule(GulpObject):
    """Class to deal with labels of atoms for GULP.
        Analyzes the hybridization and the coordination 
        of each atom to assign the correct bonds.
    """

    DEFAULT_BONDS = {
        'SINGLE': 'single',
        'DOUBLE': 'double',
        'TRIPLE': 'triple',
        'AROMATIC': 'resonant'
    }

    def __init__(self, mol, labels=MoleculeLabels()):
        self.mol = mol
        self.labels = labels

    @classmethod
    def from_smiles(cls, coords, smiles, add_hydrogens=True, labels=MoleculeLabels()):
        mol = to_mol(coords, smiles, add_hydrogens)
        return cls(mol, labels=labels)

    def get_labels(self):
        return self.labels.get_labels(self.mol)

    def get_shells(self):
        return self.labels.has_shell(self.mol)

    def get_bonds(self):
        bonds = []
        for bond in self.mol.GetBonds():
            atom_1 = bond.GetBeginAtomIdx()
            atom_2 = bond.GetEndAtomIdx()
            btype = self.DEFAULT_BONDS[str(bond.GetBondType())]
            # GULP starts counting on 1
            bonds.append((atom_1 + 1, atom_2 + 1, btype))

        return bonds

    def get_coords(self):
        return self.mol.GetConformer().GetPositions()

    def get_species(self):
        return [
            atom.GetSymbol()
            for atom in self.mol.GetAtoms()
        ]

    def get_structure(self):
        return Molecule(
            species=self.species,
            coords=self.coords,
            site_properties={'gulp_labels': self.get_labels()}
        )

    def get_lattice(self):
        return None


def to_mol(coords, smiles, add_hydrogens=True):
    mol = MolFromSmiles(smiles)
    if add_hydrogens:
        mol = Chem.AddHs(mol)

    conformer = Conformer(len(coords))
    for i, xyz in enumerate(coords):
        conformer.SetAtomPosition(i, xyz)
    
    mol.AddConformer(conformer)

    return mol


