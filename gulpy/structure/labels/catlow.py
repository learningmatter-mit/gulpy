from pymatgen.core import Site


class CatlowLabels:
    def __call__(self, site: Site) -> str:
        """Return the label of the given site

        Args:
            site (pymatgen site)
        
        Returns:
            label (str)
        """
        return site.species_string

    def has_shell(self, label: bool):
        return False
