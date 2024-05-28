#!/usr/bin/python3

import subprocess
import sys
import os

def main():
    path = os.path.expanduser("~/data.tar.gz")
    ret = os.path.exists(path)

    if ret:
        # Create temp folder.
        subprocess.run("mkdir -p /tmp/step10/", shell=True)
        
        try:
            # Check if the tarball contains all the correct contents.
            subprocess.run(f"tar -xvzf {path} -C /tmp/step10", shell=True, check=True)

            # Checking if all files are in there.
            files = ["output.txt", "output_copy.txt", "lists/", "lists/list1.txt", "lists/list2.txt", "lists/listdiff.txt"]
            for name in files:
                if not os.path.exists("/tmp/step10/" + name):
                    subprocess.run("rm -r /tmp/step10", shell=True)
                    # A file doesn't exist.
                    sys.exit(2)

            subprocess.run("rm -rf /tmp/step10", shell=True)
            # All files exist.
            sys.exit(1)
        
        except subprocess.CalledProcessError:
            # Not a valid .tar.gz file type.
            sys.exit(3)
    else:
        # Tarball not created.
        sys.exit(0)

main()
