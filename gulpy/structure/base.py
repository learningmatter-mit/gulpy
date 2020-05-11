class GulpObject:
    def get_bonds(self):
        raise NotImplementedError

    def get_labels(self):
        raise NotImplementedError

    def get_shells(self):
        raise NotImplementedError

    def get_structure(self):
        raise NotImplementedError

    def get_coords(self):
        raise NotImplementedError

    def get_species(self):
        raise NotImplementedError

    def get_lattice(self):
        raise NotImplementedError

    def __add__(self, other):
        from .joint import JointStructure
        return JointStructure([self, other])

    def __len__(self):
        return len(self.get_species())

