import os
from .options import is_reserved, is_comment


class Library:
    def __init__(self, lines):
        self.lines = lines

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as f:
            contents = [line.rstrip() for line in f]

        return cls(contents)

    @classmethod
    def from_gulp(cls, library_name):
        path = os.environ('GULP_LIB', None)
        assert path is not None, \
            "$GULP_LIB not defined. Please export this variable \
            before using `from_gulp` method"

        return cls.from_file(os.path.join(path, library_name))

    def __str__(self):
        return '\n'.join(self.get_library())

    @property
    def species_available(self):
        species = []
        start = self.lines.index('species') + 1
        for line in self.lines[start:]:
            if is_reserved(line):
                break

            species.append(line.split(' ')[0])

        return set(species)

    def get_library(self, species=None):
        """Gets a library tailored to the given species. Particularly useful
            if dealing with a custom library or avoiding certain species types.
        
        Args:
            species (list/set of str): contains all species to be considered in the library
        """

        if species is None:
            species = self.species_available

        species_lines = self.get_lines_with_species(species)
        clean_lines = self.review_lines(species_lines)

        return clean_lines 
    
    def get_lines_with_species(self, species):
        def contains_removable_species(line, to_remove):
            return any([
                species in line 
                for species in to_remove
            ])

        to_remove = set(self.species_available) - set(species)
        return [
            line for line in self.lines
            if not contains_removable_species(line, to_remove)
        ]
   
    def review_lines(self, lines):
        previous_line = '#'
        lines_saved = []
        for current_line in lines:
            if not is_comment(previous_line):
                if not (is_reserved(current_line) and is_reserved(previous_line)):
                    lines_saved.append(previous_line)

            previous_line = current_line

        if not (is_reserved(current_line) and is_reserved(previous_line)):
            lines_saved.append(previous_line)

        return lines_saved
