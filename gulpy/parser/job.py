import re
from .base import Parser


class JobParser(Parser):
    def is_completed(self):
        for line in reversed(self.lines)[:5]:
            if 'Job Finished' in line:
                return True

        return False

    def is_converged(self):
        raise NotImplementedError

    def get_version(self):
        for line in self.lines:
            if "Version = " in line:
                program = "GULP"
                version = re.findall("Version = (.*) \* Last modified.*$", line)[0]
                return program, version

        raise ParseError("GULP version not found")

    def get_duration(self):
        for line in reversed(self.lines):
            if "Total CPU time" in line:
                # PW wall clock timing is printed in a variable format:
                #   8m21.31s WALL
                #   1h 4m WALL
                time = re.findall("(\d*\.\d*)", line)[0]
                return float(time)

        raise ParseError("Job duration not found")

    def get_nprocs(self):
        for line in self.lines:
            if "Number of CPUs" in line:
                return int(re.findall("(\d+)", line)[0])

        raise ParseError("Number of CPUs not found")
