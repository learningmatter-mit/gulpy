from rdkit.Chem import Mol, Atom
from pymatgen.core import Structure

from .base import Labels, MoleculeLabels


class DreidingLabels(Labels):
    DEFAULT_LABELS = {
        "H": "H_",
        "B": "B_3",
        "C": "C_3",
        "N": "N_3",
        "O": "O_3",
        "F": "F_",
        "Cl": "Cl",
        "Br": "Br",
        "I": "I_",
        "Al": "Al3",
        "Si": "Si3",
        "P": "P_3",
        "S": "S_3",
        "Ga": "Ga3",
        "Ge": "Ge3",
        "As": "As3",
        "Se": "Se3",
        "In": "In3",
        "Sb": "Sb3",
        "Te": "Te3",
        "Na": "Na",
        "Ca": "Ca",
        "Fe": "Fe",
        "Zn": "Zn",
        "Ti": "Ti",
        "Tc": "Tc",
        "Ru": "Ru",
    }

    def get_labels(self, structure: Structure) -> list:
        return [self.DEFAULT_LABELS[site.species_string] for site in structure.sites]


class DreidingMoleculeLabels(MoleculeLabels):
    """DREIDING atom types for an rdkit molecule.

    The type of an atom is *not* its symbol with a hybridization suffix glued on:
    only B, C, N, O, P and S are written that way.  The halogens keep bare types
    (``Cl``, ``Br``), the heavier main-group elements use a suffix with no
    underscore (``Si3``, ``Al3``) and the metals are just their symbol.  The
    authoritative list is at the top of ``$GULP_LIB/dreiding.lib``, and the
    tables below are transcribed from it.

    Emitting a type the library does not define is worse than failing: GULP
    silently drops every potential mentioning it, so the atom contributes no
    valence and no van der Waals term and the total energy comes out wrong
    rather than absent.  Anything with no DREIDING type raises instead.
    """

    #: Elements that carry an explicit hybridization suffix, ``X_1``/``X_2``/``X_3``.
    ATOMS_WITH_HYBRIDIZATION = ["B", "C", "N", "O", "P", "S"]

    #: The hybridizations DREIDING actually parametrises, per element.  Sulfur
    #: and phosphorus have a single sp3 type by design (Mayo 1990 gives one
    #: ``S_3``/``P_3`` and no alternatives), so a sulfone or a sulfoxide clamps
    #: onto it rather than inventing an ``S_2`` that no potential would match.
    ALLOWED_HYBRIDIZATIONS = {
        "B": ("2", "3"),
        "C": ("1", "2", "3"),
        "N": ("1", "2", "3"),
        "O": ("1", "2", "3"),
        "P": ("3",),
        "S": ("3",),
    }

    #: Type for an aromatic atom.  Only C, N and O have a resonant type; aromatic
    #: sulfur (thiophene) and phosphorus fall back to sp3, and aromatic boron to
    #: sp2, since ``S_R``, ``P_R`` and ``B_R`` do not exist in the library.
    AROMATIC_LABELS = {
        "B": "B_2",
        "C": "C_R",
        "N": "N_R",
        "O": "O_R",
        "P": "P_3",
        "S": "S_3",
    }

    #: Elements whose type is not ``symbol`` + ``_`` + hybridization.
    FIXED_LABELS = {
        "F": "F_",
        "Cl": "Cl",
        "Br": "Br",
        "I": "I_",
        "Al": "Al3",
        "Si": "Si3",
        "Ga": "Ga3",
        "Ge": "Ge3",
        "As": "As3",
        "Se": "Se3",
        "In": "In3",
        "Sn": "Sn3",
        "Sb": "Sb3",
        "Te": "Te3",
        "Na": "Na",
        "Ca": "Ca",
        "Fe": "Fe",
        "Zn": "Zn",
        "Ti": "Ti",
        "Tc": "Tc",
        "Ru": "Ru",
    }

    def get_labels(self, mol: Mol) -> list:
        return [self.get_atom_label(atom) for atom in mol.GetAtoms()]

    def get_atom_label(self, atom: Atom):
        symbol = atom.GetSymbol()

        if self.is_hydrogen(atom):
            return "H" + self.get_hydrogen_hybridization(atom)

        if self.has_hybridization(atom):
            if atom.GetIsAromatic():
                return self.AROMATIC_LABELS[symbol]
            return "%s_%s" % (symbol, self.get_dreiding_hybridization(atom))

        if symbol in self.FIXED_LABELS:
            return self.FIXED_LABELS[symbol]

        raise ValueError(
            "No DREIDING atom type for element %r (atom %d). The types the force "
            "field defines are listed at the top of $GULP_LIB/dreiding.lib."
            % (symbol, atom.GetIdx())
        )

    def get_dreiding_hybridization(self, atom: Atom):
        """rdkit's hybridization, clamped onto one DREIDING parametrises."""
        hyb = self.get_hybridization(atom)
        allowed = self.ALLOWED_HYBRIDIZATIONS[atom.GetSymbol()]
        if hyb in allowed:
            return hyb
        return min(allowed, key=lambda h: abs(int(h) - int(hyb)))

    def get_hydrogen_hybridization(self, atom: Atom):
        if self.is_hydrogen_bonding(atom):
            return "___A"
        else:
            return "_"

    def is_hydrogen_bonding(self, atom: Atom):
        return any([nbr.GetSymbol() in ["N", "O", "S"] for nbr in atom.GetNeighbors()])

    def has_hybridization(self, atom: Atom):
        symbol = atom.GetSymbol()
        return symbol in self.ATOMS_WITH_HYBRIDIZATION
