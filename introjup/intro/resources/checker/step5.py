#!/usr/bin/python3
import subprocess
import filecmp
import os
import sys

def main():
    check_file = os.path.expanduser("~/sowpods.txt")
    verify_file = os.path.expanduser("~/sowpods_copy.txt")
    try:
        url = "https://raw.githubusercontent.com/jesstess/Scrabble/master/scrabble/sowpods.txt"
        subprocess.run(["wget", "-qO", "sowpods_copy.txt", url], check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(3)

    if (not os.path.exists(check_file)):
        subprocess.run(["rm", "-f", verify_file])
        sys.exit(2)
    elif (filecmp.cmp(check_file, verify_file)):
        subprocess.run(["rm", "-f", verify_file])
        sys.exit(0)
    else:
        subprocess.run(["rm", "-f", verify_file])
        sys.exit(1)

main()
