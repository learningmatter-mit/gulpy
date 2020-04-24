import os
from chemconfigs.gulp.dreiding import DREIDING_PARAMETERS


DEFAULT_RTOL = 1.3


class DreidingLibrary:
    """Class to create a dreiding library file with only the essential labels"""
    TYPES_TO_REMOVE = [
        'H___b', 'C_34', 'C_33', 'C_32', 'C_31',
        'C_22', 'C_21', 'C_R2', 'C_R1', 'C_11',
        'inversion squared bond kcal only3'
    ]
    ALL_TYPES = [ 'H_',     'H___A',  'H___b',  'B_3',    'B_2',    'C_34',   'C_33',   'C_32',   'C_31',   'C_3',    'C_22',   'C_21',   'C_2',    'C_R2',   'C_R1',   'C_R',    'C_11',   'C_1',    'N_3',    'N_R',    'N_2',    'N_1',    'O_3',    'O_R',    'O_2',    'O_1',    'F_',      'Cl',      'Br',      'I_',      'Al3',    'Si3',    'P_3',    'S_3',    'Ga3',    'Ge3',    'As3',    'Se3',    'In3',    'Sn3',    'Sb3',    'Te3',    'Na',     'Ca',     'Fe',     'Zn',     'Ti',     'Tc',     'Ru' ]
    TYPES_TO_RENAME = {}

    OPTIONS = ['harmonic', 'three-body', 'torsion', 'epsilon', 'lennard', 'inversion', 'hydrogen-bond']

    def __init__(self):
        self.lines = DREIDING_PARAMETERS.splitlines()

    def change_rtol(self, rtol=DEFAULT_RTOL):
        for idx, line in enumerate(self.lines):
            if 'rtol' in line:
                rtol_idx = idx
                break

        self.lines[rtol_idx] = 'rtol %.2f\n' % rtol

    def contains_bad_type(self, line, bad_types):
        return any([
            bad_type in line 
            for bad_type in bad_types
        ])

    def rename_line(self, line):
        newline = line
        for key, val in self.TYPES_TO_RENAME.items():
            if key in line:
                newline = newline.replace(key, val)

        return newline

    def create_clean_library(self, species):
        """Removes unnecessary lines from the dreiding.lib
            file from GULP.

        Args:
            species (list or set of str): each element is a species
                written as in the dreiding library.
        """
        bad_types = [
            x for x in self.ALL_TYPES
            if x not in species
        ]

        lines_saved = []
        for idx, line in enumerate(self.lines):
            if not self.contains_bad_type(line, bad_types):
                if idx > 0 and self.continues_from_previous_line(self.lines[idx - 1]):
                    if not self.contains_bad_type(self.lines[idx - 1], bad_types):
                        lines_saved.append(line)
                else:
                    lines_saved.append(line)

        clean_lines = self.review_lines(lines_saved)
        return '\n'.join(clean_lines)

    def continues_from_previous_line(self, previous_line):
        return '&' in previous_line

    def review_lines(self, lines):
        previous_line = ''
        lines_saved = []
        for current_line in lines:
            if not self.is_option(current_line):
                lines_saved.append(previous_line)
            elif not self.is_option(previous_line):
                lines_saved.append(previous_line)
            previous_line = current_line

        if not self.is_option(previous_line):
            lines_saved.append(previous_line)

        return lines_saved

    def is_option(self, line):
        return any([
            opt in line 
            for opt in self.OPTIONS
        ])
