#!/usr/bin/python3

import subprocess
import sys
import os

def main():
    path = sys.argv[1] # file for which we want to test

    # Check to see if the text file is made:
    ret = os.path.exists(path)

    # If the file is made...
    if ret:
        # Check to see if the permissions are correct.
        mode = os.stat(path).st_mode
        permissions = oct(mode)[-3:]
        if (permissions == '777'):
            sys.exit(2)
        else:
            sys.exit(1)
    else:
        sys.exit(0)

main()
