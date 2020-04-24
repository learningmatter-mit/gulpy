import os
import subprocess


GULP_CMD = os.environ['GULP']


def run_gulp(inp, out, stdout):
    output = subprocess.check_output(
        ' '.join([GULP_CMD, f'< {inp}', f'> {out}']),
        stderr=subprocess.STDOUT,
        shell=True
    ).decode()

    with open(stdout, 'w+') as f:
        f.write(output)
        


