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

    # TODO: implement better way to write bonds in crystals
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
        return self.labels.get_labels(self.structure)

    def get_shells(self):
        return self.labels.has_shell(self.structure)

    def get_renamed_structure(self):
        gulp_labels = self.get_labels()
        has_shell = self.get_shells()

        return Structure(
            species=self.structure.species,
            coords=self.structure.cart_coords,
            lattice=self.structure.lattice.matrix,
            coords_are_cartesian=True,
            site_properties={'gulp_labels': gulp_labels, 'has_shell': has_shell}
        )

