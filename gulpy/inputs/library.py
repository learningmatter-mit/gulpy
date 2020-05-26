import os

from gulpy.parser import Parser
from gulpy.structure import labels
from .options import is_reserved, is_comment


class Library(Parser):
    @classmethod
    def from_gulp(cls, library_name):
        path = os.environ.get("GULP_LIB", None)
        assert (
            path is not None
        ), "$GULP_LIB not defined. Please export this variable \
            before using `from_gulp` method"

        return cls.from_file(os.path.join(path, library_name))

    def __str__(self):
        return "\n".join(self.get_library())

    @property
    def species(self):
        species = []
        start = self.lines.index("species") + 1
        for line in self.lines[start:]:
            if is_reserved(line):
                break

            element = line.split(" ")[0]
            if element != "":
                species.append(element)

        return set(species)

    def get_library(self, species=None):
        """Gets a library tailored to the given species. Particularly useful
            if dealing with a custom library or avoiding certain species types.
        
        Args:
            species (list/set of str): contains all species to be considered in the library
        """

        if species is None:
            species = self.species

        species_lines = self.get_lines_with_species(species)
        clean_lines = self.review_lines(species_lines)

        return clean_lines

    def get_lines_with_species(self, species):
        def contains_removable_species(line, to_remove):
            return any([species in line for species in to_remove])

        to_remove = set(self.species) - set(species)

        return self.break_ampersand([
            line
            for line in self.join_ampersand(self.lines)
            if not contains_removable_species(line, to_remove)
        ])

    def join_ampersand(self, lines):
        text = "\n".join(lines)
        return text.replace("&\n", "& ").splitlines()

    def break_ampersand(self, lines):
        text = "\n".join(lines)
        return text.replace("& ", "&\n").splitlines()

    def review_lines(self, lines):
        previous_line = "#"
        lines = self.remove_comments(lines)
        lines_saved = []
        for current_line in lines:
            if not (is_reserved(current_line) and is_reserved(previous_line)):
                lines_saved.append(previous_line)

            previous_line = current_line

        if not is_reserved(previous_line):
            lines_saved.append(previous_line)

        return lines_saved[1:]

    def remove_comments(self, lines):
        return [line for line in lines if not is_comment(line)]


class LibraryLabels:
    STRUCT_LABELS = {
        'catlow.lib': labels.CatlowLabels,
        'dreiding.lib': labels.DreidingLabels,
    }

    MOLECULE_LABELS = {
        'dreiding.lib': labels.DreidingMoleculeLabels,
    }

    @staticmethod
    def get_labels(library, is_molecule=False):
        labels = LibraryLabels.MOLECULE_LABELS if is_molecule else LibraryLabels.STRUCT_LABELS
        return labels[library]()

