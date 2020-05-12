from gulpy.parser import JobParser, MolecularDynamicsParser
from .base import Job


class MDParser(MolecularDynamicsParser, JobParser):
    pass


class MDJob(Job):
    @property
    def __name__(self):
        return "md"

    @property
    def parser(self):
        return MDParser

    def parse_results(self, out, traj_file):
        parser = self.parser.from_file(out, traj_file)
        return {
            key: getattr(parser, attr)()
            for key, attr in self.parse_opts.items()
        }
