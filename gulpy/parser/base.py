import re
import pandas as pd


FLOAT_REGEX = "(-?\d+(?:\.\d+)?)"
INT_REGEX = "(-?\d+)"


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

    def find_pattern(self, pattern):
        """Finds all occurences of a given pattern throughout all lines"""
        return re.findall(pattern, '\n'.join(self.lines))

    def parse_float(self, line):
        """Returns the first float from a line"""
        return float(re.findall(FLOAT_REGEX, line)[0])

    def parse_vector(self, line):
        return [ float(x)
            for x in re.findall(FLOAT_REGEX, line)
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

