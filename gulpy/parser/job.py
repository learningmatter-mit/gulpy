import re
from .base import Parser, ParseError, FLOAT_REGEX, INT_REGEX


class JobParser(Parser):
    def is_completed(self):
        try:
            idx, _ = self.find_line("Job Finished")
            return True
        except ParseError:
            return False

    def has_error(self):
        try:
            idx, _ = self.find_line("!! ERROR :")
            return True
        except ParseError:
            return False

    def get_version(self):
        return self.find_pattern("Version = (.*) \* Last modified.*")[0]

    def get_host(self):
        host = self.find_pattern("Host name\s+= (.*)")

        if len(host) > 0:
            return host[0]

        return None

    def get_duration(self):
        return float(self.find_pattern("Total CPU time\s+%s" % FLOAT_REGEX)[-1])

    def get_nprocs(self):
        return int(self.find_pattern("Number of CPUs =\s+%s" % INT_REGEX)[-1])
