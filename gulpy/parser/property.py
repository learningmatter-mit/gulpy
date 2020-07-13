import re
import pandas as pd

from .base import ParseError, FLOAT_REGEX
from .structure import StructureParser


class PropertyParser(StructureParser):
    def get_total_energy(self):
        energies = self.find_pattern("Total lattice energy\s+=\s+%s eV" % FLOAT_REGEX)

        if len(energies) > 0:
            return float(energies[-1])

        raise ParseError("Total energy not found in output")

    def get_forces(self):
        """Get forces and convert their unit to Ha/bohr"""
        try:
            idx, _ = self.find_line("Final internal derivatives")
        except ParseError:
            idx, _ = self.find_line("Final Cartesian derivatives")

        table = pd.DataFrame(
            self.parse_columns(
                self.lines[idx + 6 : idx + 6 + self.num_atoms], [1, 3, 4, 5]
            ),
            columns=["label", "x", "y", "z"],
        )

        forces = table[["x", "y", "z"]].applymap(float).values.tolist()

        return forces

    def get_gnorm(self):
        _, line = self.find_line("Final Gnorm")
        return self.parse_float(line)

    def get_stress(self):
        """Get stresses and convert their unit to Ha/bohr^3"""
        raise NotImplementedError
