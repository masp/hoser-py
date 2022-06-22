
import subprocess
import sys
import tempfile
from hoser.compile import Pipe, Stream, exec
from hoser.serialize import serialize
import os
import argparse


def run(pipe: Pipe):
    """run will compile the given pipe and execute it using the hoser executable as a subprocess piping stdio"""
    parser = argparse.ArgumentParser(description="Compiles and runs program: " + pipe.name)
    parser.add_argument("-o", type=str, help='file path to output compiled JSON to')
    args, unknown = parser.parse_known_args()

    pipes = [pipe]
    pipes += pipe.all_children()
    compiled = serialize(*pipes)
    if args.o:
        with open(args.o, 'w') as tmp:
            tmp.write(compiled)
    else:
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(compiled.encode("utf-8"))
            tmp.seek(0)
            result = subprocess.run(["hoser"]+unknown+[tmp.name], stdin=sys.stdin, stderr=sys.stderr, stdout=sys.stdout)
            sys.exit(result.returncode)


def run_lines(lines: Stream, pipe: Pipe, err=False, varname="line"):
    """run_lines will execute 'pipe' for each line in the input passed as a variable called 'varname'"""
    return exec("hoser", args=["run", f"$SELF:{pipe.name}", "-sep", "\n", "-var", varname], stdin=lines, stderr=err)

        