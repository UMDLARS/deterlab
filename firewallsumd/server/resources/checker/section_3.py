#!/usr/bin/python3
import sys
import os
import re
import subprocess

def main():
    # Checks usage.
    if (len(sys.argv) != 3):
        print("Usage: ./section_3.py <step> <answer>")
        sys.exit(2)

    step = sys.argv[1]
    answer = sys.argv[2]

    # Check Step 9
    if (step == "9"):
        if (answer == "-t filters"):
            # Correct answer. Save the response so that other steps can refer to it.
            f = open("/home/.checker/responses/step_9_answer.txt", "w+")
            f.write(answer)
            f.close()
            sys.exit(1)

        else:
            sys.exit(0)

    # Check Step 10.
    if (step == "10"):
        # Need a regular expression for checking this step.
        if (answer == "-o eth1 -A OUTPUT" or answer == "-A OUTPUT -o eth1"):
            # Correct answer. Save the response so that other steps can refer to it.
            f = open("/home/.checker/responses/step_10_answer.txt", "w+")
            f.write(answer)
            f.close()
            sys.exit(1)

        else:
            sys.exit(0)

    # Check Step 11.
    if (step == "11"):
        # Need a regular expression for checking this step.
        if (answer == "-m state --state NEW -p tcp" or answer == "-p tcp -m state --state NEW"):
            # Correct answer. Save the response so that other steps can refer to it.
            f = open("/home/.checker/responses/step_11_answer.txt", "w+")
            f.write(answer)
            f.close()
            sys.exit(1)

        else:
            sys.exit(0)

    # Check Step 12.
    if (step == "12"):
        # NOTE: Google's IP address changes depending on which server that gets pinged.
        # To allow this step to work over the world, get some "wildcard" IP addresses.
        ips = []
        for i in range(10):
            result = subprocess.run("dig google.com +short", shell=True, capture_output=True, text=True)
            # Get the first part of the network ID.
            split_ip = (result.stdout.strip()).split('.')
            network_id = '.'.join(split_ip[:2])
            if (network_id not in ips):
                ips.append(network_id)

        # Check Step 12.
    if (step == "12"):
        # NOTE: Google's IP address changes depending on which server that gets pinged.
        # To allow this step to work over the world, get some "wildcard" IP addresses.
        ips = []
        for i in range(10):
            result = subprocess.run("dig google.com +short", shell=True, capture_output=True, text=True)
            # Get the first part of the network ID.
            split_ip = (result.stdout.strip()).split('.')
            network_id = '.'.join(split_ip[:2])
            if (network_id not in ips):
                ips.append(network_id)

        # Additionally, get the IP from telnet, since it may sometimes not appear from dig.
        process = subprocess.Popen(["telnet", hostname], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        ip_address = None

        # Read the output with a limited number of attempts.
        for _ in range(max_attempts):
            output = process.stdout.readline()
            if "Trying" in output:
                # Extract the IP address using a regular expression.
                match = re.search(r"Trying\s+([\d\.]+)\s*", output)
                if match:
                    ip_address = match.group(1)
                    break

        ips.append(ip_address)

        # Terminate the process.
        process.terminate()
        process.wait()

        # All potential IPs that the student can use are now in an array. Check to see if any of them
        # are used in the students answer.
        for ip in ips:
            # Student is using a valid IP for Google. Now, use a regular expression to check the rest of
            # the student's answer.
            print(ips)
            if (ip in answer):
                pattern = r"(?=.*-s 10\.0\.1\.1)(?=.*-d " + re.escape(ip) + r"\.\d+\.\d+)(?=.*--dport 1234)"
                # Student has all three, required parameters for the step. IP address likely matches the one
                # pulled from the dig command.
                if (re.search(pattern, answer)):
                    # Everything matches. Save and end successfully.
                    f = open("/home/.checker/responses/step_12_answer.txt", "w")
                    f.write(answer)
                    f.close()

                    sys.exit(1)

        # If the student reaches here, there was never a complete match. Likely due to the incorrect IP
        # address, or not everything was constructed properly.
        sys.exit(0)


    # Check Step 13.
    if (step == "13"):
        # This should be pretty self-explanatory.
        if (answer == "-j DROP"):
            f = open("/home/.checker/responses/step_13_answer.txt", "w")
            f.write(answer)
            f.close()
            sys.exit(1)

        else:
            sys.exit(0)


main()
