class GulpObject:
    def get_bonds(self):
        raise NotImplementedError

    def get_labels(self):
        raise NotImplementedError

    def get_shells(self):
        raise NotImplementedError

    def get_labels_with_shells(self):
        labels = self.get_labels()
        shells = self.get_shells()

        labels_with_shells = []
        core_shell = []
        for label, has_shell in zip(labels, shells):
            labels_with_shells += [label] * (2 if has_shell else 1)
            core_shell += ['core', 'shell'] if has_shell else ['core']

        return labels_with_shells, core_shell

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

