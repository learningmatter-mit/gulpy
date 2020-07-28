import re
import pandas as pd
from rdkit.Chem import AllChem as Chem
from pymatgen.core import Structure, Molecule


from .base import Parser, ParseError


PERIODIC_TABLE = Chem.GetPeriodicTable()


class StructureParser(Parser):
    def __init__(self, lines):
        super().__init__(lines)
        self.num_atoms = self.get_num_atoms()

    def get_num_atoms(self):
        _, line = self.find_line("Total number atoms/shells")
        return self.parse_int(line)

    def get_num_molecules(self):
        _, line = self.find_line("Total number of molecules")
        return self.parse_int(line)

    def get_volume(self):
        _, line = self.find_line("Initial cell volume")
        return self.parse_vector(line)[0]

    def get_dimensionality(self):
        _, line = self.find_line("Dimensionality =")
        return self.parse_int(line)

    def is_bulk(self) -> bool:
        return self.get_dimensionality() == 3

    def get_lattice(self, input=False):
        if not self.is_bulk():
            return []

        if input:
            idx, _ = self.find_line("Cartesian lattice vectors (Angstroms)")
        else:
            idx, _ = self.find_line("Final Cartesian lattice vectors (Angstroms) :")

        return self.parse_matrix(self.lines[idx + 2 : idx + 5])

    def get_structure_table(self, input=False, include_shell=False):
        coords_type = "Fractional" if self.is_bulk() else "Cartesian"
        if input:
            idx, _ = self.find_line(f"{coords_type} coordinates")
        else:
            idx, _ = self.find_line(f"Final {coords_type.lower()} coordinates of atoms")

        table = pd.DataFrame(
            self.parse_columns(
                self.lines[idx + 6 : idx + 6 + self.num_atoms], [1, 2, 3, 4, 5]
            ),
            columns=["label", "cs", "x", "y", "z"],
        )
        table[["x", "y", "z"]] = table[["x", "y", "z"]].applymap(float)

        if not include_shell:
            table = table[table["cs"] == "c"]

        return table

    def get_coords(self, input=False, include_shell=False):
        table = self.get_structure_table(input, include_shell)

        if not include_shell:
            table = table[table["cs"] == "c"]

        labels = table["label"].values.tolist()
        coords = table[["x", "y", "z"]].applymap(float).values.tolist()

        return labels, coords

    def get_species_labels(self):
        idx, _ = self.find_line("Species output for all configurations")

        label_to_symbol = {}
        for line in self.lines[idx + 6 :]:
            if "-------" in line:
                break

            row = self.parse_row(line)
            label, atomic_num = row[0], int(row[2])

            symbol = PERIODIC_TABLE.GetElementSymbol(atomic_num)
            label_to_symbol[label] = symbol

        return label_to_symbol

    def get_pymatgen_structure(self):
        if not self.is_bulk():
            return self.get_pymatgen_molecule()

        try:
            lattice = self.get_lattice()
        except ParseError:
            lattice = self.get_lattice(input=True)

        try:
            labels, frac_coords = self.get_coords()
        except ParseError:
            labels, frac_coords = self.get_coords(input=True)

        renamer = self.get_species_labels()
        symbols = [renamer[l] for l in labels]

        return Structure(
            lattice=lattice,
            species=symbols,
            coords=frac_coords,
            site_properties={"gulp_labels": labels},
        )

    def get_pymatgen_molecule(self):
        try:
            labels, cart_coords = self.get_coords()
        except ParseError:
            labels, cart_coords = self.get_coords(input=True)

        renamer = self.get_species_labels()
        symbols = [renamer[l] for l in labels]

        return Molecule(
            species=symbols,
            coords=cart_coords,
            site_properties={"gulp_labels": labels},
        )
