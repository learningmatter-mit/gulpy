import numpy as np
import networkx as nx
from networkx.algorithms.traversal.depth_first_search import dfs_edges

from typing import List

from pymatgen.core import Molecule, Structure
from pymatgen.analysis.graphs import StructureGraph
from pymatgen.analysis.local_env import JmolNN


class MoleculeExtractor:
    def __init__(
        self, structure: Structure,
    ):
        """Extracts a molecule from a pymatgen Structure using the given indices.
            Useful when the molecule crosses the boundary of the unit cell and
            the atoms are disconnected when the information on the lattice is ignored.
        """
        self.structure = structure

    def get_molecular_structure_from_indices(self, indices: List[int]) -> Structure:
        return Structure(
            species=[sp for i, sp in enumerate(self.structure.species) if i in indices],
            coords=self.structure.cart_coords[indices],
            lattice=self.structure.lattice.matrix,
            coords_are_cartesian=True,
        )

    def get_structure_graph(self, struct: Structure) -> nx.Graph:
        sgraph = StructureGraph.with_local_env_strategy(struct, JmolNN())
        return sgraph

    def walk_graph_and_get_coords(self, sgraph: StructureGraph) -> np.array:
        vectors = self.get_distance_vectors(sgraph)
        node_coords = {0: sgraph.structure[0].coords}
        for u, v in dfs_edges(nx.Graph(sgraph.graph), source=0):
            node_coords[v] = node_coords[u] + vectors[(u, v)]

        final_coords = np.array([node_coords[k] for k in sorted(node_coords.keys())])

        return final_coords

    def get_distance_vectors(self, sgraph: StructureGraph) -> dict:
        """Creates the distance vectors between connected nodes.
            Useful when walking through the graph later.
        """
        distance_vectors = {}
        for u in sgraph.graph.nodes:
            ucoords = sgraph.structure[u].coords
            for conn_site in sgraph.get_connected_sites(u):
                v = conn_site.index
                vcoords = conn_site.site.coords
                distance_vectors[(u, v)] = vcoords - ucoords

        return distance_vectors

    def extract_molecule(self, indices: List[int]) -> Molecule:
        struct = self.get_molecular_structure_from_indices(indices)
        sgraph = self.get_structure_graph(struct)
        coords = self.walk_graph_and_get_coords(sgraph)

        return Molecule(species=struct.species, coords=coords)
