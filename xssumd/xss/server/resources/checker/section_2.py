#!/usr/bin/python3
import os
import subprocess
import sys

def main():
    if (len(sys.argv) != 2):
        print("Usage: ./section_2.py <step_num>")
        sys.exit(0)

    step = sys.argv[1]

    # Each of these steps need to call a JavaScript file.
    if (step == "2"):
        # Run the section_2.js file within the docker container.
        result = subprocess.run("sudo docker run section_2 2", shell=True, capture_output=True, text=True)

        # Check to see if there was an error.
        if (result.stderr != ""):
            sys.exit(2)

        # Otherwise, get the output and check it.
        if (result.stdout == "62\n"):
            sys.exit(1)

        else:
            sys.exit(0)

    elif (step == "3"):
        # Run the section_2.js file within the docker container.
        result = subprocess.run("sudo docker run section_2 3", shell=True, capture_output=True, text=True)

        # To check this step, access the victim's page and save the page's contents.
        subprocess.run("sudo docker run section_2 3", shell=True, capture_output=True, text=True)
main()
