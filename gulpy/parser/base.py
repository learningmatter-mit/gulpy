import re
import pandas as pd


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, lines):
        self.lines = lines

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as f:
            contents = [line.strip() for line in f]

        return cls(contents)

    def find_line(self, text):
        """Finds the first line that contains the given text"""
        for idx, line in enumerate(self.lines):
            if text in line:
                return idx, line

        raise ParseError("{} not found in lines".format(text))

    def parse_vector(self, line):
        return [ float(x)
            for x in re.findall("(-?\d+(?:\.\d+)?)", line)
        ]
    
    def parse_matrix(self, lines):
        return [
            self.parse_vector(line)
            for line in lines
        ]

    def parse_row(self, line):
        return line.strip().split()

    def parse_table(self, lines):
        return [self.parse_row(line) for line in lines]

    def parse_columns(self, lines, columns):
        table = pd.DataFrame(self.parse_table(lines))
        return table.iloc[:, columns].values.tolist()




class GulpParser(Parser):
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
