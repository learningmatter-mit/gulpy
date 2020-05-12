from gulpy.parser import JobParser, PropertyParser
from .base import Job


class SingleParser(JobParser, PropertyParser):
    pass


class SingleJob(Job):
    @property
    def __name__(self):
        return "single"

    def parse_results(self, out):
        parser = SingleParser.from_file(out)

        return {
            'job': {
                'duration': parser.get_duration(),
                'nprocs': parser.get_nprocs(),
                'completed': parser.is_completed(),
                'version': parser.get_version()
            },
            'properties': {
                'energy': parser.get_total_energy()
            }
        }

