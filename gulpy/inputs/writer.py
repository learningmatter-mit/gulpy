class FileWriter:
    def __init__(self):
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'<FileWriter base class>'

    def write_file(self, filename):
        with open(filename, "w") as f:
            f.write(self.__str__())


class InputWriter(FileWriter):
    def __init__(
        self,
        keywords,
        options,
        structure,
        library,
        *args,
        title='',
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.keywords = keywords
        self.options = options
        self.structure = structure
        self.library = library
        self.title = title

    def __repr__(self):
        return '<{} with keywords: {}>'.format(
            self.__class__.__name__,
            ' '.join(self.keywords)
        )

    def _render_keywords(self):
        return ' '.join(self.keywords)

    def _render_title(self):
        return """title\n {}\nend\n""".format(self.title)

    def _render_options(self):
        options_str = ['{} {}'.format(opt, val) for opt, val in self.options.items()]
        return '\n'.join(options_str)

    def _render_lattice(self):
        lattice = self.structure.get_lattice()
        if lattice is not None:
            vectors = '\n'.join([
                '%.7f %.7f %.7f' % tuple(row.tolist())
                for row in lattice
            ])
            return """\nvectors\n{} \n""".format(vectors)
        return "\n"

    def _render_coords(self):
        def format_coords(label, xyz):
            return '{:>5} {:>10.5f} {:>10.5f} {:>10.5f}'.format(
                label, xyz[0], xyz[1], xyz[2]
            )

        coords = self.structure.get_coords()
        labels = self.structure.get_labels()

        coord_lines = '\n'.join([
            format_coords(label, xyz)
            for label, xyz in zip(labels, coords)
        ])

        return """cartesian\n{}\n""".format(coord_lines)

    def _render_library(self):
        return str(self.library)

    def _render_extras(self):
        return ''

    def _render_bonds(self):
        def format_bonds(tup):
            return 'connect %d %d %s' % tup

        return '\n'.join([
            format_bonds(tup)
            for tup in self.structure.get_bonds()
        ])
    
    def __str__(self):
        return '\n'.join([
            self._render_keywords(),
            self._render_title(),
            self._render_options(),
            self._render_lattice(),
            self._render_coords(),
            self._render_bonds(),
            self._render_extras(),
            self._render_library()
        ])
