import re
import numpy as np
import pandas as pd

from pymatgen.core import Structure
from pymatgen.core.trajectory import Trajectory

from .base import Parser, ParseError
from .structure import StructureParser


class MolecularDynamicsParser(StructureParser):
    def __init__(self, lines, traj_lines):
        super().__init__(lines)
        self.traj_lines = traj_lines
        self.num_atoms = self.get_num_atoms()

    @classmethod
    def from_file(cls, output_file, traj_file):
        with open(output_file, "r") as f:
            output = [line.strip() for line in f]

        with open(traj_file, "r") as f:
            trajectory = [line.strip() for line in f]

        return cls(output, trajectory)
        frames = re.findall(
            "#  Coordinates\n(.*?)#  Velocities", self.traj_lines, re.DOTALL
        )

    def __len__(self):
        return len(self.get_step_props())

    def get_md_table(self, pattern):
        text = "\n".join(self.traj_lines)
        frames = re.findall(pattern, text, re.DOTALL)

        return [np.array(self.parse_matrix(lines.splitlines())) for lines in frames]

    def get_section(self, name):
        """gets a section of the `.trg` file containing the given name"""
        return self.get_md_table("#  %s\n(.*?)(?:#|$)" % name)

    def get_coords(self):
        return self.get_section("Coordinates")

    def get_md_cell(self):
        """Get all cells from the MD simulation. If the ensemble has constant
            volume, all cells are equal.

        Returns:
            cells (list of np.array)
            constant_lattice (bool)
        """
        cells = self.get_section("Cell")
        if len(cells) == len(self):
            return cells, False

        elif len(cells) == 0:
            return [self.get_lattice(input=True)] * len(self), True

        raise ParseError("Invalid number of cells")

    def get_velocities(self):
        return self.get_section("Velocities")

    def get_forces(self):
        return self.get_section("Derivatives")

    def get_site_energies(self):
        frame_energies = self.get_section("Site energies")
        return [e.reshape(-1) for e in frame_energies]

    def get_step_props(self):
        steps = self.get_section("Time/KE/E/T")

        df = pd.DataFrame(
            np.concatenate(steps),
            columns=["time", "kinetic_energy", "total_energy", "temperature"],
        ).applymap(float)

        return df

    def get_md_props(self, include_shell=False):
        table = self.get_structure_table(input=True, include_shell=include_shell)

        forces = [x[table.index] for x in self.get_forces()]
        vels = [x[table.index] for x in self.get_velocities()]
        energies = [x[table.index].sum() for x in self.get_site_energies()]
        props = self.get_step_props()
        traj = self.get_pymatgen_trajectory(include_shell)

        return [
            {
                "structure": struct,
                "potential_energy": en,
                "time": time,
                "forces": f,
                "temperature": temp,
                "velocities": v,
            }
            for struct, en, time, f, temp, v in zip(
                traj, energies, props.time, forces, props.temperature, vels
            )
        ]

    def get_pymatgen_trajectory(self, include_shell=False):
        table = self.get_structure_table(input=True, include_shell=include_shell)

        lattices, constant_lattice = self.get_md_cell()

        frames = [x[table.index] for x in self.get_coords()]
        time = self.get_step_props()["time"]
        time_step = time[1] - time[0]

        species_labels = self.get_species_labels()
        symbols = table["label"].map(species_labels).values.tolist()

        structures = [
            Structure(
                lattice=lattice,
                species=symbols,
                coords=coords,
                coords_are_cartesian=True,
                site_properties={"gulp_labels": table["label"]},
            )
            for lattice, coords in zip(lattices, frames)
        ]

        return Trajectory.from_structures(
            structures, time_step=time_step, constant_lattice=constant_lattice
        )
