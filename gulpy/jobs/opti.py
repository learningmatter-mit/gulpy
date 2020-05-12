from gulpy.parser import JobParser, PropertyParser, StructureParser
from .base import Job


class OptiParser(JobParser, PropertyParser, StructureParser):
    pass


class OptiJob(Job):
    @property
    def __name__(self):
        return "opti"

    @property
    def parser(self):
        return OptiParser
