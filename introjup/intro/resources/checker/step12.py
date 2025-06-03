#!/usr/bin/python3
import os
import sys
import subprocess
import time

def main():
    if len(sys.argv) != 2:
        sys.exit(2)

    # Required file paths.
    nums = os.path.expanduser("~/numbers.txt")
    sorted_nums = os.path.expanduser("~/sortednumbers.txt")
    input_command = sys.argv[1]

    # Commands that are not allowed.
    bad_commands = ["rm", "mv"]
    # Commands that are required.
    required_commands = ["grep", "sort", "|"]

    # Check for disallowed commands.
    if any(bad in input_command for bad in bad_commands):
        sys.exit(3)

    # Check for required commands presence.
    if not all(req in input_command for req in required_commands) or "|" not in input_command:
        sys.exit(3)

    # Clear the sortednumbers.txt file, if it exists.
    if os.path.exists(sorted_nums):
        os.remove(sorted_nums)

    # Run the command.
    result = subprocess.run(input_command, shell=True, text=True, capture_output=True)

    # Wait a moment for the file to write from the student's input.
    time.sleep(1)

    if os.path.exists(sorted_nums):
        # Retrieve the original numbers.
        with open(nums, "r") as orig_file:
            orig_list = orig_file.readlines()

        # Retrieve the student's answer.
        with open(sorted_nums, "r") as file:
            sorted_list = file.readlines()

        # Check if the sorted output is correct.
        expected_sorted = sorted([line.strip() for line in orig_list if '9' in line])
        student_sorted = [line.strip() for line in sorted_list]

        # Checks if the answer is correct.
        if expected_sorted == student_sorted:
            sys.exit(0)

        # Answer is incorrect.
        else:
            sys.exit(2)
    else:
        sys.exit(1)

main()
