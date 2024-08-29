#!/usr/bin/python3
import os
import sys
import subprocess
import time

def main():
    if (len(sys.argv) != 2):
        sys.exit(2)

    # Get the student's answer.
    nums = os.path.expanduser("~/numbers.txt")
    sorted_nums = os.path.expanduser("~/sortednumbers.txt")
    input_command = sys.argv[1]

    # Make sure that the command that the student is running isn't unsafe.
    if ("rm" in input_command or "mv" in input_command or "sort" not in input_command):
        sys.exit(3)

    # Clear the sortednumbers.txt file, if any.
    if (os.path.exists(sorted_nums)):
        os.remove(sorted_nums)

    # Run the command.
    result = subprocess.run(input_command, shell=True, text=True, capture_output=True)

    # Wait a moment for the file to write from the student's input.
    time.sleep(1)

    if (os.path.exists(sorted_nums)):
        # Retrieving the numbers.txt file:
        orig_file = open(nums, "r")
        orig_file = orig_file.readlines()

        # Retrieving the student's answer.
        file = open(sorted_nums, "r")
        sorted_list = file.readlines()

        # Checking to make sure that they're sorted.
        if (sorted(orig_file) == sorted_list):
            sys.exit(1)
        else:
            sys.exit(2)
    else:
        sys.exit(0)

main()
