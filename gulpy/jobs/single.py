from gulpy.parser import JobParser, PropertyParser
from .base import Job


class SingleParser(JobParser, PropertyParser):
    pass


class SingleJob(Job):
    @property
    def __name__(self):
        return "single"

    @property
    def parser(self):
        return SingleParser


class EngradJob(SingleJob):
    @property
    def __name__(self):
        return "engrad"
