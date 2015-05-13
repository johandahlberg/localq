#!/usr/bin/env python
import Pyro4
import sys

__author__ = 'dankle'

usage = """Usage:
    lbatch.py [-n N] sh myscript.sh
    lbatch.py [-n N] ls
    lbatch.py [-n N] python mypythonscript.py
"""

def parse_cli():
    args = sys.argv
    args.pop(0)  # remove script name itself

    if len(args) == 0:
        print usage
        sys.exit(1)

    num_cores = 1
    if args[0] == "-n":
        try:
            num_cores = int(args[1])
        except  ValueError:
            print usage
            sys.exit(1)
        args.pop(0)
        args.pop(0)

    if len(args) == 0:
        print usage
        sys.exit(1)

    return [num_cores, args]


def main():
    (num_cores, cmd) = parse_cli()
    print "Num cores requested: " + str(num_cores)
    print "command to run: " + str(cmd)

    # you have to change the URI below to match your own host/port.
    localqd = Pyro4.Proxy("PYRONAME:localqd")
    jobid = localqd.add(cmd, num_cores)
    print "Job added to the queue with id " + str(jobid)


if __name__ == "__main__":
    sys.exit(main())
