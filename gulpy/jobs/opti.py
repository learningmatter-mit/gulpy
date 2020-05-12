from gulpy.parser import JobParser, PropertyParser, StructureParser
from .base import Job


class OptiParser(JobParser, PropertyParser, StructureParser):
    pass


class OptiJob(Job):
    @property
    def __name__(self):
        return "opti"

    def parse_results(self, out):
        parser = OptiParser.from_file(out)

        return {
            'job': {
                'duration': parser.get_duration(),
                'nprocs': parser.get_nprocs(),
                'completed': parser.is_completed(),
                'version': parser.get_version()
            },
            'properties': {
                'energy': parser.get_total_energy(),
                'forces': parser.get_forces(),
                'gnorm': parser.get_gnorm(),
            },
            'structure': parser.get_pymatgen_structure()
        }

