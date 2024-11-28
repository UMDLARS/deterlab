#!/usr/bin/python3
import sys

def main():
    # Checks usage.
    if (len(sys.argv) != 3):
        print("Usage: ./section_1.py <step> <answer>")
        sys.exit(2)

    step = sys.argv[1]
    answer = ' '.join(sys.argv[2].split())

    # Check Step 1.
    if (step == "1"):
        if (answer == "nmap yahoo.com"):
            sys.exit(1)
        else:
            sys.exit(0)

    # Check Step 2.
    if (step == "2"):
        if (answer == "eth1"):
            sys.exit(1)
        else:
            sys.exit(0)

    # Check Step 3.
    if (step == "3"):
        # Split the answers.
        answers = answer.split("\\n")

        print(answers)

        # Check the two solutions.
        if (answers[0].strip() == "telnet scse.d.umn.edu 443" and answers[1].strip() == "GET /majors-minors"):
            sys.exit(1)

        else:
            sys.exit(0)

    # Check Step 4.
    if (step == "4"):
        # Split the answers.
        answers = answer.split("\\n")

        required_params = ["-l", "-p 10000"]

        other_components_present = all(component in answers[0] for component in required_params)

        # Check the two solutions.
        if (answers[0].startswith("nc") and other_components_present and answers[1] == "nc server 10000"):
            sys.exit(1)

        else:
            sys.exit(0)


main()
