#!/usr/bin/python3

import subprocess
import sys
import os

def main():
    path = os.path.expanduser("~/message.sh")

    # Check to see if the text file is made:
    ret = os.path.exists(path)

    # If the file is made...
    if ret:
        # Check to see if the permissions are correct.
        if (os.access(path, os.X_OK)):
            sys.exit(1)
        else:
            sys.exit(2)
    else:
        # File was (somehow) not made.
        sys.exit(0)

main()
