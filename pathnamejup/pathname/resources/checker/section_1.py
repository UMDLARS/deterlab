#!/usr/bin/python3
import subprocess
import sys
import os
import getpass
import time
import shutil
import grp
import re

def main():
    if (len(sys.argv) != 2):
        print("Usage: ./section_1.py <step>")
        sys.exit(2)

    step = sys.argv[1]
    user = getpass.getuser()

    # Before running this step, in case the process wasn't closed previously, do this to kill any
    # existing processes on port 5010, which is what the checker is using.
    result = subprocess.run(['lsof', '-t', f'-i:5010'], capture_output=True, text=True)
    pids = result.stdout.strip()
    if pids:
        subprocess.run(['kill', *pids.split()])

    # Check Step 2 and 3. Step 1 is not checked.
    if (step == "2" or step == "3"):
        # Navigate into the home directory.
        os.chdir("/home/" + user)

        # Check to make sure that the server can be started.
        if (not os.path.exists("/home/" + user + "/step_2.py") and step == "2" or \
            not os.path.exists("/home/" + user + "/step_3.py") and step == "3"):
            sys.exit(2)

        # Start the server on port 5010.
        process = subprocess.Popen(["python3", "-m", "flask", "--app", "step_" + step, "run", "-p", "5010"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # To prevent a race condition.
        time.sleep(2)

        # Server is running. Now, run the section_1 binary file.
        if (step == "2"):
            result = subprocess.run("/home/.checker/section_1 2", shell=True, capture_output=True, text=True)

            # End the server and get the output.
            process.terminate()

            # For debugging.
            # process_output, process_errors = process.communicate()

            if (result.returncode == 1):
                if (not os.path.exists("/home/" + user + "/step_3.py")):
                    shutil.copyfile("/home/" + user + "/step_2.py", "/home/" + user + "/step_3.py")

            # Check to see that the result is valid.
            sys.exit(result.returncode)


        # Step 3 requires sudo, as it will need to have permissions to create /lab.
        elif (step == "3"):
            result = subprocess.run("sudo /home/.checker/section_1 3", shell=True, capture_output=True, text=True)

            # After running the result, check to see if /lab is owned by sudo. If it is, then we will need to change permissions.
            if (os.path.exists("/lab")):
                stat_info = os.stat('/lab')
                uid = stat_info.st_uid

                if (uid == 0):
                    subprocess.run("sudo chown -R " + user + " /lab", shell=True)

            # End the server and get the output.
            process.terminate()

            # For debugging.
            process_output, process_errors = process.communicate()

            # Check to see that the result is valid.
            sys.exit(result.returncode)

    # Check Step 4 and 5.
    elif (step == "4" or step == "5"):
        # This file should've already been made.
        if (not os.path.exists("/lab/memo.py")):
            sys.exit(2)

        # Navigate into the /lab directory.
        os.chdir("/lab")

        # Start the server on port 5010.
        process = subprocess.Popen(["python3", "-m", "flask", "--app", "memo", "run", "-p", "5010"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # To prevent a race condition.
        time.sleep(2)

        f = open("/lab/memo.py", "r")
        content = f.read()
        f.close()

        # For debugging.
        # process_output, process_errors = process.communicate()

        # print(process_output)
        # print(process_errors)

        # Step 4 will do regex matching before testing.
        if (step == "4"):
            # Get the pattern.
            pattern = r'\s*return\s+redirect\s*\(\s*url_for\s*\(\s*[\'"]index[\'"]\s*\)\s*\)'

            # If the student already has an answer, use the pattern above and do a separate check.
            if (os.path.exists("/home/.checker/responses/step_4_response.txt")):
                f = open("/home/.checker/responses/step_4_response.txt", "r")
                content = f.read()
                f.close()

                # Split at the divider that was made earlier. Perform matches.
                result = content.split("\n-DIVIDER-\n")
                matches = re.findall(pattern, result[0])

                if (len(matches) == 2):
                    # Successful. Now, check to make sure that the previous response was valid.
                    if ("<p>You should be redirected automatically to the target URL: <a href=\"/\">/</a>. If not, click the link." in result[1]):
                        sys.exit(1)

                    else:
                        sys.exit(0)

            else:
                # Perform a match.
                matches = re.findall(pattern, content)

                # There must be exactly two matches. If so, then the step is passed. Call ./section_1 to run the test
                # through the server and check if it works.
                if (len(matches) == 2):
                    # Save a copy of the student's answer.
                    shutil.copyfile("/lab/memo.py", "/home/.checker/responses/step_4_response.txt")

                    # Perform the check.
                    # Caution: This is going to overwrite the student's work if it's successful. This is intentional, but could make debugging hard!
                    result = subprocess.run("/home/.checker/section_1 4", shell=True, capture_output=True, text=True)

                    # If the response was successful, append the response to the text file that was just made.
                    if ("<p>You should be redirected automatically to the target URL: <a href=\"/\">/</a>. If not, click the link." in result.stdout):
                        f = open("/home/.checker/responses/step_4_response.txt", "a")
                        f.write("\n-DIVIDER-\n")
                        f.write(result.stdout)
                        sys.exit(1)

                    # Otherwise, delete the file. This wasn't correct. This shouldn't happen!
                    else:
                        os.remove("/home/.checker/responses/step_4_response.txt")
                        sys.exit(0)

                else:
                    sys.exit(0)

        # This check doesn't need to be ran in the C file.
        elif (step == "5"):
            # Check to see if this step was already completed.
            if (os.path.exists("/home/.checker/responses/step_5_response.txt")):
                with open("/home/.checker/responses/step_5_response.txt", 'r') as file:
                    content = file.read()
                    # Remove any ANSI escape codes from the content.
                    cleaned_content = re.sub(r'\x1b\[([0-9]{1,2};)?[0-9]{1,2}m', '', content)
                    # Now perform the check on the cleaned content.
                    if '"POST /delete_memo/9999 HTTP/1.1" 302' in cleaned_content:
                        sys.exit(1)

                    # This shouldn't happen. The test would "pass", but somehow not pass?
                    else:
                        sys.exit(3)

            # First, creating a test memo.
            f = open("/lab/memos/9999", "w+")
            f.write("test")
            f.close()

            # Perform a cURL call to delete it.
            result = subprocess.run("curl -X POST -v http://127.0.0.1:5010/delete_memo/9999", shell=True, text=True, capture_output=True)

            # Check the result:
            if ("Accept: */*" not in result.stderr):
                process.terminate()
                sys.exit(0)

            # Run the binary file.
            result = subprocess.run("/home/.checker/section_1 5", shell=True, capture_output=True, text=True)

            # Close the process and check the result from the pipe.
            process.terminate()
            process.wait()
            process_output, process_errors = process.communicate()

            process_errors = process_errors.strip()

            # POST was successful, but check to see if the file was actually deleted. Additionally, check if the binary file passed.
            if (not os.path.exists("/lab/memos/9999") and result.returncode == 0):
                # Successful. Finally, write the response so that it can be used later.
                f = open("/home/.checker/responses/step_5_response.txt", "w+")
                f.write(process_errors)
                f.close()

                sys.exit(1)

            # POST succeeded, but did not remove the file. Or, the output that the binary file tested for was incorrect.
            else:
                if (os.path.exists("/lab/memos/9999")):
                    os.remove("/lab/memos/9999")

                sys.exit(0)


    else:
        sys.exit(2)

main()
