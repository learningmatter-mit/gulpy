import re

from .base import Parser, ParseError


class StructureParser(Parser):
    def __init__(self, lines):
        super().__init__(lines)
        self.num_atoms = self.get_num_atoms()

    def get_num_atoms(self):
        _, line = self.find_line("Total number atoms/shells")
        return int(self.parse_vector(line)[0])

    def get_volume(self):
        _, line = self.find_line("Initial cell volume")
        return self.parse_vector(line)[0]

    def get_lattice(self):
        idx, _ = self.find_line('Final Cartesian lattice vectors (Angstroms) :')

        return self.parse_matrix(self.lines[idx + 2:idx + 5])

    def get_input_lattice(self):
        idx, _ = self.find_line('Cartesian lattice vectors (Angstroms)')
        return self.parse_matrix(self.lines[idx + 2:idx + 5])

    # TODO: test this
    def get_frac_coords(self):
        idx, _ = self.find_line('Final fractional coordinates of atoms')
        table = pd.DataFrame(self.parse_columns(self.lines[idx + 6:idx + 6 + self.num_atoms], [1, 3, 4, 5]), columns=['label', 'x', 'y', 'z'])

        labels = table['label'].values.tolist()
        coords = table[['x', 'y', 'z']].applymap(float).values.tolist()

        return labels, coords

    # TODO: test this
    def get_input_frac_coords(self):
        idx, _ = self.find_line('Fractional coordinates')
        table = pd.DataFrame(self.parse_columns(self.lines[idx + 6:idx + 6 + self.num_atoms], [1, 3, 4, 5]), columns=['label', 'x', 'y', 'z'])

        labels = table['label'].values.tolist()
        coords = table[['x', 'y', 'z']].applymap(float).values.tolist()

        return labels, coords

    # TODO: fix this
    def get_structure(self, get_input=False):
        if get_input:
            lattice = get_input_lattice(self.lines)
            labels, frac_coords = get_input_frac_coords(self.lines)
        else:
            lattice = get_lattice(self.lines)
            labels, frac_coords = get_frac_coords(self.lines)

        renamer = get_species_labels(self.lines)
        symbols = [renamer[l] for l in labels]

        cart_coords = np.array(frac_coords) @ np.array(lattice)
        cart_coords = cart_coords.tolist()

        coords = []
        for sym, xyz in zip(symbols, cart_coords):
            coords.append({
                'element': sym,
                'x': xyz[0],
                'y': xyz[1],
                'z': xyz[2]
            })

        return lattice, coords

    def get_pymatgen_structure(self):
        from pymatgen.core import Structure

        lattice = self.get_lattice(self.lines)

        labels, frac_coords = self.get_frac_coords(self.lines)
        renamer = self.get_species_labels(self.lines)
        symbols = [renamer[l] for l in labels]

        if lattice is not None:
            return Structure(
                lattice=lattice,
                species=symbols,
                coords=frac_coords
            )

    def get_species_labels(self):
        idx, _ = self.find_line('Species output for all configurations')

        label_to_symbol = {}
        for line in self.lines[idx + 6:]:
            if '-------' in line:
                break

            # TODO: fix this
            label = line.split()[0]
            atomic_num = int(line.split()[2])
            symbol = PERIODIC_TABLE.GetElementSymbol(atomic_num)

            label_to_symbol[label] = symbol

        return label_to_symbol


class PropertyParser(Parser):

    def get_total_energy(self):
        """Gets final total energy and converts the unit (eV) to Hartree"""
        for line in reversed(self.self.lines):
            if "Total lattice energy" in line and "eV" in line:
                return float(
                    re.findall("(-?\d+(?:\.\d+)?)", line)[0]
                )

        raise ParseError("Total energy not found in output")

    def get_forces(self):
        """Get forces and convert their unit to Ha/bohr"""
        force_line = None
        for idx, line in enumerate(self.lines):
            if 'Final internal derivatives' in line:
                force_line = idx + 6

        if force_line is None:
            return

        num_atoms = get_num_atoms(self.lines)

        forces = []
        for line in self.lines[force_line:force_line + num_atoms]:
            forces.append([
                float(x) * eVperAngs
                for x in re.findall("\s+(-?\d+(?:\.\d+)?)", line)[1:4]
            ])

        return forces

    def get_stress(self):
        """Get stresses and convert their unit to Ha/bohr^3"""
        raise NotImplementedError



