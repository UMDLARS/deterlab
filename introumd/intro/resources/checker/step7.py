#!/usr/bin/python3

import subprocess
import sys
import os

def main():
    path = sys.argv[1] # directory for which we want to test

    ret = os.path.exists(path)

    if ret:
        sys.exit(1)
    else:
        sys.exit(0)

main()
