#!/usr/bin/python3
import subprocess
import sys
import os

def main():
    # Check to make sure that the copied file exists.
    orig_file = os.path.expanduser("~/Important Data/output.txt")
    copy_file = os.path.expanduser("~/Important Data/output_copy.txt")
    new_dir = os.path.expanduser("~/Important Data/lists")
    target_file = os.path.expanduser("~/Important Data/lists/list1.txt")

    # Check if the file was made yet.
    if (not os.path.exists(copy_file)):
        sys.exit(0)

    # File was made.
    else:
        # Check if the files are the same.
        output = subprocess.run(f'diff -q "{orig_file}" "{copy_file}" > /dev/null', shell=True)
        if (output.returncode == 0):
            # Files are the same.
            # For the next step:
            subprocess.run(f'bash ~/../.checker/create_files.sh "{new_dir}" "{target_file}"', shell=True)
            sys.exit(1)
        # Files are NOT the same.
        else:
            sys.exit(2)

    sys.exit(3)
main()
