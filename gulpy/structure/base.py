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

    def get_property_with_shells(self, method_name):
        props = getattr(self, method_name)()
        shells = self.get_shells()

        props_with_shells = []
        core_shell = []
        for prop, has_shell in zip(props, shells):
            props_with_shells += [prop] * (2 if has_shell else 1)
            core_shell += ["core", "shell"] if has_shell else ["core"]

        return props_with_shells, core_shell

    def get_labels_with_shells(self):
        return self.get_property_with_shells("get_labels")

    def get_coords_with_shells(self):
        return self.get_property_with_shells("get_coords")

    def get_labels_shells_coords(self):
        labels, core_shell = self.get_labels_with_shells()
        coords, _ = self.get_coords_with_shells()

        return labels, core_shell, coords

    def get_species(self):
        raise NotImplementedError

    def get_lattice(self):
        raise NotImplementedError

    def __add__(self, other):
        from .joint import JointStructure

        return JointStructure([self, other])

    def __len__(self):
        return len(self.get_species())
