#!/usr/bin/python3
import subprocess
import sys
import os
import time
import re

def main():
    # Check the usage.
    if len(sys.argv) != 3:
        print("Usage: ./section_4.py <step_num> <payload>")
        sys.exit(2)

    # Create the step/payload.
    step = sys.argv[1]
    payload = sys.argv[2]

    # Get the student's username from the last line of /etc/passwd.
    with open('/etc/passwd') as f:
        for line in f:
            pass
        last_line = line
        username = last_line.split(":")[0]

    # Step 17, 19, and 20 are the steps that can be properly tested.
    if (step != "18"):
        # Create the Wormwood directory so that we can navigate into it.
        # There's a strange glitch where ./run.sh won't work unless you're in the directory.
        wormwood_dir = f"/home/" + username + "/topic_4"

        # The file that needs to be called to use Wormwood.
        wormwood = f"{wormwood_dir}/run.sh"

        # Specific to Step 17.
        if (step == "17"):
            try:
                # Change the working directory to where run.sh is located.
                os.chdir(wormwood_dir)

                # Start the process.
                process = subprocess.Popen([wormwood], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                try:
                    # Send 'a' without newline.
                    process.stdin.write("a")
                    process.stdin.flush()
                    time.sleep(0.5)
                    # print("Sent 'a' to the process")

                    # Send the payload without newline.
                    process.stdin.write(payload)
                    process.stdin.flush()
                    time.sleep(0.5)
                    # print(f"Sent payload: {payload}")

                    # Send three newline characters to press "enter".
                    for _ in range(3):
                        process.stdin.write("\n")
                        process.stdin.flush()
                        time.sleep(0.5)
                        # print("Sent newline")

                    # Get the output and error with a timeout.
                    output, error = process.communicate(timeout=10)  # Timeout in seconds

                    # If the program reaches here, then the program exited. We can see if it crashed.
                    if ("The reactor failed catastrophically" in output):
                        sys.exit(1)

                    # If it doesn't crash, exit it with 0.
                    else:
                        sys.exit(0)

                # If the timer expires, then the program never crashed.
                except subprocess.TimeoutExpired:
                    process.terminate()
                    sys.exit(2)

            except Exception as e:
                print(f"An error occurred: {e}", file=sys.stderr)
                sys.exit(2)

        elif (step == "19" or step == "20"):
            # Splitting the "double new line".
            payload = payload.replace('\\n', '\n')
            payloads = payload.split('\n')
            filtered_payloads = [item for item in payloads if item]

            try:
                # Change the working directory to where run.sh is located.
                os.chdir(wormwood_dir)

                # Start the process.
                process = subprocess.Popen([wormwood], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                try:
                    # Send 'a' without newline.
                    process.stdin.write("a")
                    process.stdin.flush()
                    # print("Sent 'a' to the process")
                    time.sleep(0.5)

                    # Send 'super' without newline.
                    process.stdin.write("super")
                    process.stdin.flush()
                    # print("Sent 'super' to the process")
                    time.sleep(0.5)

                    # Send a newline character.
                    process.stdin.write("\n")
                    process.stdin.flush()
                    # print("Sent 'new line' to the process")
                    time.sleep(0.5)

                    for i in range(0, len(filtered_payloads)):
                        # Send the payload.
                        process.stdin.write(filtered_payloads[i])
                        process.stdin.flush()
                        # print(f"Sent {filtered_payloads[i]} to the process.")
                        time.sleep(0.5)

                        if (i == 0 or i == 2):
                            # Send a newline character.
                            process.stdin.write("\n")
                            process.stdin.flush()
                            # print("Sent 'new line' to the process")
                            if (i == 0):
                                time.sleep(0.5)
                            elif (i == 2):
                                time.sleep(10)

                    # Send another newline character.
                    process.stdin.write("\n")
                    process.stdin.flush()
                    # print("Sent 'new line' to the process")
                    time.sleep(0.5)

                    # Get the output and error with a timeout.
                    output, error = process.communicate(timeout=30)  # Increased timeout to 30 seconds

                    # If the program reaches here, then the program exited. We can see if it crashed.
                    if "The reactor failed catastrophically" in output:
                        sys.exit(1)

                    # If it doesn't crash, exit it with 0.
                    else:
                        print("Process completed successfully.")
                        sys.exit(0)

                # If the timer expires, then the program never crashed.
                except subprocess.TimeoutExpired:
                    process.terminate()
                    print("Timed out!")
                    output, error = process.communicate()  # Retrieve whatever output is available
                    print("Output from the process:")
                    print(output)
                    print("Error from the process:")
                    print(error, file=sys.stderr)
                    sys.exit(2)

            except Exception as e:
                print(f"An error occurred: {e}", file=sys.stderr)
                sys.exit(2)


    # Checks Step 18.
    elif (step == "18"):
        # Gets the user input. Using regular expressions to check the answer here.
        pattern = r"^(\%s\s*){8,}$"

        if (re.search(pattern, payload)):
            sys.exit(1)

        else:
            sys.exit(0)


main()
