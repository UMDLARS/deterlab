#!/usr/bin/python3
import subprocess
import sys
import os

def main():
    # Check to make sure that the copied file exists.
    orig_file = os.path.expanduser("~/Important Data/output.txt")
    copy_file = os.path.expanduser("~/Important Data/output_copy.txt")

    # Check if the file was made yet.
    if (not os.path.exists(copy_file)):
        sys.exit(0)

    # File was made.
    else:
        # Check if the files are the same.
        output = subprocess.run(f"diff -q \"{orig_file}\" \"{copy_file}\" > /dev/null", shell=True, executable='/bin/bash')
        if (output.returncode == 1):
            # Files are not the same.
            sys.exit(1)
        # Files are the same. Check to see if the files share the same creation time.
        else:
            output = subprocess.run(f"diff -q <(stat \"{orig_file}\" | grep Access) <(stat \"{copy_file}\" | grep Access) > /dev/null", shell=True, executable='/bin/bash')
            if (output.returncode == 1):
                # Two files do not have the same creation time.
                sys.exit(2)
            else:
                sys.exit(3)

    sys.exit(4)
main()
