from pymatgen.core import Structure
from pymatgen.analysis.graphs import StructureGraph
from pymatgen.analysis.local_env import CutOffDictNN

from .labels import Labels


class GulpCrystal:
    """Class to deal with labels of crystals for GULP.
    """
    def __init__(self, structure, labels=Labels()):
        self.structure = structure
        self.labels = labels

    def get_bonds(self):
        graph = StructureGraph.with_local_env_strategy(
            self.structure,
            CutOffDictNN({('Si', 'O'): 2.0, ('O', 'Si'): 2.0})
        )

        # GULP starts counting on 1
        return [
            (u + 1, v + 1, 'single')
            for u, v in graph.graph.edges()
        ]

    def get_labels(self):
        return [
            self.labels(atom.species_string)
            for atom in self.structure.sites
        ]

    def get_renamed_structure(self):
        return Structure(
            species=self.structure.species,
            coords=self.structure.cart_coords,
            lattice=self.structure.lattice.matrix,
            coords_are_cartesian=True,
            site_properties={'gulp_labels': self.get_labels()}
        )

