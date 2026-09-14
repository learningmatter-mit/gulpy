import os
import sys
import subprocess


GULP_CMD = os.environ["GULP"]

def run_gulp(inp, out, stdout):
    print(f'\ngulpy/jobs/runtime.py - DEBUG: {" ".join([GULP_CMD, f"< {inp}", f"> {out}"])}')
    try:
        output = subprocess.check_output(
            " ".join([GULP_CMD, f"< {inp}", f"> {out}"]),
            stderr=subprocess.STDOUT,
            shell=True,
        ).decode()
    except subprocess.CalledProcessError as e:
        print(f"ERROR: return code {e.returncode}")
        print(f"ERROR: {e.output}")
        sys.exit()

    with open(stdout, "w+") as f:
        f.write(output)

    return output
