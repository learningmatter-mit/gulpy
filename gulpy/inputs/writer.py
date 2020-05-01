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


class GulpInput(FileWriter):
    def __init__(
        self,
        keywords,
        options,
        structure,
        library,
        *args,
        title='',
        bonds=None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.keywords = keywords
        self.options = options
        self.structure = structure
        self.library = library
        self.title = title
        self.bonds = bonds

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
        if hasattr(self.structure, 'lattice'):
            vectors = '\n'.join([
                '%.7f %.7f %.7f' % tuple(row.tolist())
                for row in self.structure.lattice.matrix
            ])
            return """\nvectors\n{} \n""".format(vectors)
        return "\n"

    def _render_coords(self):
        def line_from_site(site):
            return '{:>5} {:>10.5f} {:>10.5f} {:>10.5f}'.format(
                site.properties['gulp_labels'], site.x, site.y, site.z
            )

        coord_lines = '\n'.join([line_from_site(site) for site in self.structure.sites])
        return """cartesian\n{}\n""".format(coord_lines)

    def _render_library(self):
        return self.library

    def _render_extras(self):
        return ''

    def _render_bonds(self):
        def line_from_tuple(tup):
            return 'connect %d %d %s' % tup

        if self.bonds is None:
            return ''

        return '\n'.join([
            line_from_tuple(tup)
            for tup in self.bonds
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

    @classmethod
    def from_gulpjobspec(cls, gulpspec):
        return cls(
            gulpspec.keywords,
            gulpspec.options,
            gulpspec.structure,
            gulpspec.library
        )
