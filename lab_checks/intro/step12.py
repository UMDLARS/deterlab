#!/usr/bin/python3
import os
import sys

def main():
    # Get the student's answer.
    nums = os.path.expanduser("~/numbers.txt")
    sorted_nums = os.path.expanduser("~/sortednumbers.txt")

    if (os.path.exists(sorted_nums)):
        # Retrieving the student's answer.
        file = open(sorted_nums, "r")
        sorted_list = file.readlines()

        # Sorting the numbers.txt file:
        orig_file = open(nums, "r")
        orig_file = orig_file.readlines()

        # Checking to make sure that they're sorted.
        if (sorted(orig_file) == sorted_list):
            sys.exit(1)
        else:
            sys.exit(2)
    else:
        sys.exit(0)

main()
