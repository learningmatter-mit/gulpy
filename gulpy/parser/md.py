import re
import numpy as np
import pandas as pd

from .base import Parser, ParseError
from .structure import StructureParser


class MolecularDynamicsParser(StructureParser):
    def __init__(self, lines, traj_lines):
        super().__init__(lines)
        self.traj_lines = traj_lines
        self.num_atoms = self.get_num_atoms()

    @classmethod
    def from_file(cls, output_file, traj_file):
        with open(output_file, 'r') as f:
            output = [line.strip() for line in f]

        with open(traj_file, 'r') as f:
            trajectory = [line.strip() for line in f]

        return cls(output, trajectory)
        frames = re.findall("#  Coordinates\n(.*?)#  Velocities", self.traj_lines, re.DOTALL)

    def get_frames(self):
        text = '\n'.join(self.traj_lines)
        frames = re.findall("#  Coordinates\n(.*?)#  Velocities",text, re.DOTALL)

        return [
            np.array(self.parse_matrix(lines.splitlines()))
            for lines in frames
        ]

    def get_step_properties(self):
        text = '\n'.join(self.traj_lines)
        steps = re.findall("#  Time/KE/E/T\n(.*?)#  Coordinates", text, re.DOTALL)
        df = pd.DataFrame(
            self.parse_table(steps),
            columns=['time', 'kinetic_energy', 'total_energy', 'temperature']
        )
        df = df.applymap(float)
        return df

    def get_trajectory(self):
        frames = self.get_frames()

        if not include_shell:
            table = table[table['cs'] == 'c']

        labels = table['label'].values.tolist()
        coords = table[['x', 'y', 'z']].applymap(float).values.tolist()

        return labels, coords

