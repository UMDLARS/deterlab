#!/usr/bin/python3
import subprocess
import sys
import os
import re

def main():
    if (len(sys.argv) != 3):
        print("Usage: ./section_2.py <step> <input>")
        sys.exit(2)

    step = sys.argv[1]
    input = sys.argv[2]

    # Checking Steps 6 through 9.
    if 6 <= int(step) <= 9:
        pattern = ''

        if (step == "6"):
            pattern = r'^(posts\/..\/){0,1}(\.\.\/){3,}etc\/passwd(/){0,1}$'

        elif (step == "7"):
            pattern = r'^(\.\.\/){4,}etc\/passwd(/){0,1}$'

        elif (step == "8"):
            pattern = r'^\/etc\/passwd$'

        elif (step == "9"):
            pattern = r'^((posts%2F){0,1}(\.\.%2F){4,}etc%2Fpassword)|(%2Fetc%2Fpasswd)$'

        matches = re.findall(pattern, input)
        if (matches):
            sys.exit(0)

        else:
            sys.exit(1)

    else:
        sys.exit(2)

main()
