import json
import numpy as np

from chemconfigs.gulp.labels import DreidingTypes, DEFAULT_LABELS
from docking.zeolite.molecule import MoleculeDetector
from pymatgen.core import Structure, Molecule, DummySpecie
from pymatgen.analysis.graphs import StructureGraph
from pymatgen.analysis.local_env import CutOffDictNN


class GulpJobspec:
    def __init__(self, jobspec):
        self.jobspec = jobspec.copy()
        self._library = self.jobspec["details"]["library"]

    def check_input(self):
        assert self.jobspec["details"]["library"] == "dreiding.lib"

    @classmethod
    def from_json(cls, json_file):
        with open(json_file, "r") as f:
            jobspec = json.load(f)
        return cls(jobspec)

    @property
    def structure(self):
        symbols = [c["element"] for c in self.jobspec["coords"]]
        xyz = np.array([[c["x"], c["y"], c["z"]] for c in self.jobspec["coords"]])
        lattice = self.jobspec["details"].get("lattice", None)

        if lattice is not None:
            return Structure(
                species=symbols, coords=xyz, lattice=lattice, coords_are_cartesian=True
            )
        else:
            return Molecule(species=symbols, coords=xyz)

    @property
    def keywords(self):
        kwds = self.jobspec["details"].get("keywords", []).copy()
        kwds.append("conv" if self.jobspec["details"]["fix_cell"] else "conp")
        return kwds

    @property
    def options(self):
        opts = {}
        opts["maxcyc"] = self.jobspec["details"]["max_steps"]
        return opts

    @property
    def library(self):
        return self._library

    @library.setter
    def library(self, value):
        self._library = value


class DockingJobspec(GulpJobspec):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.smiles = self.get_smiles()
        self.molecule_indices = self.get_molecules()
        self.substrate_indices = self.get_substrate()

    def get_smiles(self):
        return self.jobspec["details"].get("ligand", None)

    def get_molecules(self):
        moldetect = MoleculeDetector(self.structure)

        if "molecule" in self.jobspec["details"]:
            indices = []
            for smiles, idx in self.jobspec["details"]["molecule"]:
                if moldetect.detect_smiles_from_idx(smiles, idx) != []:
                    indices.append(idx)
        else:
            indices = moldetect.detect_molecules()

        return indices

    def get_substrate(self):
        """Get indices of the substrate."""
        mol_indices = [x for sublist in self.molecule_indices for x in sublist]
        return [idx for idx in range(len(self.structure)) if idx not in mol_indices]

    def get_molecule_labels(self):
        if self.smiles is None:
            return {}

        labels = {}
        for indices in self.molecule_indices:
            xyz = self.structure.cart_coords[indices]

            dreiding_labeler = DreidingTypes(self.smiles, xyz)

            mol_labels = dreiding_labeler.get_labels()

            labels = {**labels, **dict(zip(indices, mol_labels))}

        return labels

    def get_substrate_labels(self):
        symbols = [str(self.structure.species[i]) for i in self.substrate_indices]
        gulp_symbols = [DEFAULT_LABELS[x] for x in symbols]
        return dict(zip(self.substrate_indices, gulp_symbols))

    def get_all_labels(self):
        labels = {**self.get_molecule_labels(), **self.get_substrate_labels()}
        return {k: labels[k] for k in sorted(labels)}

    def get_coords_with_new_symbols(self, labels):
        gulp_coords = [
            {
                "element": labels[atom_idx],
                "x": atom["x"],
                "y": atom["y"],
                "z": atom["z"],
            }
            for atom_idx, atom in enumerate(self.jobspec["coords"])
            if atom_idx in labels
        ]
        return gulp_coords

    def get_all_coords(self):
        labels = self.get_all_labels()
        return self.get_coords_with_new_symbols(labels)

    def get_ligand_coords(self):
        labels = self.get_molecule_labels()
        return self.get_coords_with_new_symbols(labels)

    def get_substrate_coords(self):
        labels = self.get_substrate_labels()
        return self.get_coords_with_new_symbols(labels)

    def get_molecule_bonds(self, is_complex=True):
        if self.smiles is None:
            return []

        bonds = []
        cumsum = 0
        for indices in self.molecule_indices:
            xyz = self.structure.cart_coords[indices]

            dreiding_labeler = DreidingTypes(self.smiles, xyz)

            mol_bonds = dreiding_labeler.get_bonds()

            if is_complex:
                bonds += [
                    (indices[u] + 1, indices[v] + 1, btype) for u, v, btype in mol_bonds
                ]
            else:
                bonds += [
                    (u + 1 + cumsum, v + 1 + cumsum, btype) for u, v, btype in mol_bonds
                ]
                cumsum += len(indices)

        return bonds

    def get_substrate_bonds(self, is_complex=True):
        graph = StructureGraph.with_local_env_strategy(
            self.substrate, CutOffDictNN({("Si", "O"): 2.0, ("O", "Si"): 2.0})
        )

        if is_complex:
            return [
                (self.substrate_indices[u] + 1, self.substrate_indices[v] + 1, "single")
                for u, v in graph.graph.edges()
            ]
        else:
            return [(u + 1, v + 1, "single") for u, v in graph.graph.edges()]

    def get_all_bonds(self):
        return self.get_molecule_bonds() + self.get_substrate_bonds()

    def get_renamed_structure(self, labels):
        species = [self.structure.species[idx] for idx in labels.keys()]
        coords = [self.structure.cart_coords[idx] for idx in labels.keys()]
        return Structure(
            species=species,
            coords=coords,
            lattice=self.structure.lattice.matrix,
            coords_are_cartesian=True,
            site_properties={"gulp_labels": list(labels.values())},
        )

    def get_species_labels(self):
        labels = self.get_all_labels()
        return set(labels.values())

    @property
    def complex(self):
        labels = self.get_all_labels()
        return self.get_renamed_structure(labels)

    @property
    def ligand(self):
        labels = self.get_molecule_labels()
        return self.get_renamed_structure(labels)

    @property
    def substrate(self):
        labels = self.get_substrate_labels()
        return self.get_renamed_structure(labels)
