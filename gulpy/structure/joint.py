import numpy as np

from .base import GulpObject


flatten = lambda l: [item for sublist in l for item in sublist]


class JointStructure(GulpObject):
    def __init__(self, structures: list):
        self._check_input(structures)
        self.structures = structures

    def __add__(self, other):
        if isinstance(other, JointStructure):
            return JointStructure(self.structures + other.structures)
        elif isinstance(other, GulpObject):
            return JointStructure(self.structures + [other])

        raise ValueError(
            "object of class {} cannot be concatenated to a JointStructure".format(
                other.__class__.__name__
            )
        )

    def _check_input(self, structures):
        assert isinstance(structures, list)
        assert all([isinstance(st, GulpObject) for st in structures])

        lattices = [st.get_lattice() for st in structures]
        lattices = [x for x in lattices if x is not None]

        for lat in lattices:
            np.testing.assert_almost_equal(
                lat, np.stack(lattices, axis=-1).mean(axis=-1)
            )

    def get_joint_property(self, method_name):
        return [getattr(struct, method_name)() for struct in self.structures]

    def get_bonds(self):
        bonds = self.get_joint_property("get_bonds")
        natoms = self.get_joint_property("__len__")

        reindex = 0
        all_bonds = []
        for b, n in zip(bonds, natoms):
            for u, v, btype in b:
                all_bonds.append((u + reindex, v + reindex, btype))

            reindex += n

        return all_bonds

    def get_labels(self):
        return flatten(self.get_joint_property("get_labels"))

    def get_shells(self):
        return flatten(self.get_joint_property("get_shells"))

    def get_coords(self):
        joint_coords = self.get_joint_property("get_coords")
        return np.concatenate(joint_coords, axis=0)

    def get_species(self):
        return flatten(self.get_joint_property("get_species"))

    def get_lattice(self):
        lattices = [x for x in self.get_joint_property("get_lattice") if x is not None]
        return lattices[0]

    def get_structure(self):
        gulp_labels = self.get_labels()
        has_shell = self.get_shells()

        return Structure(
            species=self.get_species(),
            coords=self.get_coords(),
            lattice=self.get_lattice(),
            coords_are_cartesian=True,
            site_properties={"gulp_labels": gulp_labels, "has_shell": has_shell},
        )
