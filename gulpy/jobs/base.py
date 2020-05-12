import os
import yaml

from gulpy.parser import JobParser
from gulpy.inputs import InputWriter
from .runtime import run_gulp


DEFAULTS_PATH = 'defaults'

INPUT_SUFFIX = 'gin'
OUTPUT_SUFFIX = 'out'
STDOUT_SUFFIX = 'log'


class Job:
    def __init__(
        self,
        structure,
        library,
        options={}
    ):
        self.structure = structure
        self.library = library
        self.keywords, self.options, self.parse_opts = self.get_defaults()
        self.update_options(options)

    @property
    def __name__(self):
        return 'base_job'

    def get_defaults(self):
        path = os.path.join(DEFAULTS_PATH, self.__name__, ".yml")
        if not os.path.exists(path):
            return [], {}, {}

        with open(path, 'r') as f:
            defaults = yaml.safe_load(f)

        kwds = defaults.get('keywords', [])
        opts = defaults.get('options', {})
        parse_opts = defaults.get('parse', {})

        return kwds, opts, parse_opts

    def update_keywords(self, kwds):
        self.keywords = kwds

    def update_options(self, opts):
        self.options = {
            **self.options,
            **opts
        }

    def write_input(self, path):
        writer = InputWriter(
            self.keywords,
            self.options,
            self.structure,
            self.library,
            self.__name__
        )

        with open(path, 'w') as f:
            f.write(str(writer))

    def run(self, inp):
        out = inp.replace(INPUT_SUFFIX, OUTPUT_SUFFIX)
        stdout = inp.replace(INPUT_SUFFIX, STDOUT_SUFFIX)
        log = run_gulp(inp, out, stdout)

        self.handle_errors(log)

        return out, stdout

    def handle_errors(self, log):
        pass

    @property
    def parser(self):
        return JobParser

    def parse_results(self, out):
        parser = self.parser.from_file(out)
        return {
            key: getattr(parser, attr)
            for key, attr in self.parse_opts.items()
        }
