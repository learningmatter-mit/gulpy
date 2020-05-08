from collections import defaultdict
from pymatgen.core import Site, Structure

from .base import Labels


class CatlowLabels(Labels):
    CUTOFF_NEIGHBOR = 1.8
    ELEMENTS = ['Na', 'Mg', 'Al', 'Si', 'P', 'O', 'H']

    def has_shell(self, structure: Structure):
        return [
            label == 'O_O2-'
            for label in self.get_labels(structure)
        ]

    def get_labels(self, structure: Structure):
        return [
            self.get_site_label(structure, site)
            for site in structure.sites
        ]

    def get_site_label(self, structure: Structure, site: Site):
        assert site.species_string in self.ELEMENTS, "element {} not in SLC library".format(site.species_string)
        
        if site.species_string == 'H':
            return 'H_OH'

        elif site.species_string == 'O':
            return self.get_oxygen_label(structure, site)

        return site.species_string

    def get_oxygen_label(self, structure: Structure, site: Site):
        nbrs = structure.get_neighbors(site, self.CUTOFF_NEIGHBOR)
        if any([nbr.species_string == 'H' for nbr in nbrs]) and len(nbrs) == 2:
            return 'O_OH'
        
        return 'O_O2-'


