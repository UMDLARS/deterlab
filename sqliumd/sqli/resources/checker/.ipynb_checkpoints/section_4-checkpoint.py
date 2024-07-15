#!/usr/bin/python3
import subprocess
import os
import sys
import re
import requests

def main():
    # Checking the usage:
    if (len(sys.argv) != 3):
        print("Usage: ./section_4 <step_num> <query>")
        print(len(sys.argv))
        sys.exit(2)

    step = sys.argv[1]
    query = sys.argv[2]

    # Checking Step 16 and 17: Accessing accounts through SQLi.
    if (step == "16" or step == "17"):
        # First, applying some checks to the user input.
        # Checks to see if the student may be typing an ID into the payload.
        if (re.search("[0-9]{3,}", query)):
            sys.exit(3)

        # Checks to see if they forgot to use a SQL comment.
        if (not re.search("--", query)):
            sys.exit(4)

        # SQLi attempt appears to be valid. Now, construct the POST request.
        url = 'http://localhost/cgi-bin/FCCU.php'

        # Defining the payload, as well as the step number for each payload.
        data = {
            'id': query,
            'password': "asdf"
        }

        # Send the POST request.
        response = requests.post(url, data=data)

        # Check if the request was successful.
        if (response.status_code == 200):
            # If the request was successful, write the response to a text file to show the student.
            # Only snag the account information table. We don't want to flood the notebook with output.
            f = open("/home/.checker/responses/step_" + step + "_response.txt", "w+")
            # A regular expression that captures all tables in the output.
            pattern = re.compile(r'<table\b.*?</table>', re.DOTALL)
            # Getting all tables in the response.
            match = pattern.findall(response.text)

            # The table with the account information is the second table (index 1) in the output.
            if (match):
                # Check to see if this match contains "Account Information".
                if ("Account Information" in match[1]):
                    # If it does, then the SQLi passes. However, do one more check for Step 17.
                    f.write(match[1])
                    f.close()

                    if (step == "16"):
                        sys.exit(1)

                    elif (step == "17"):
                        # First, check to see if the previous step wasn't completed.
                        # This was already checked in the notebook, so this shouldn't occur.
                        if (not os.path.exists("/home/.checker/responses/step_16_response.txt")):
                            sys.exit(5)

                        # If the file exists, compare it with the current response. It MUST be different!
                        else:
                            prev_response = open("/home/.checker/responses/step_16_response.txt", "r")

                            # Check to see if the new response matches the previous response.
                            if (match[1] == prev_response.read()):
                                # SQLi was correct, but did not return another user.
                                sys.exit(6)

                            # Otherwise, correct. Response was already written.
                            else:
                                sys.exit(1)

                # This occurs if a table was produced, but an account wasn't successfully signed in.
                # SQLi payload failed.
                else:
                    sys.exit(0)

            # If no tables are being produced, then the SQLi fails.
            else:
                sys.exit(0)

        # Otherwise, the HTTP request did not work.
        else:
            print("Error")
            sys.exit(2)

    # Step 18: Wiping a bank account.
    elif (step == "18"):
        if (not os.path.exists("/home/.checker/responses/wire_logs.txt")):
            # A transfer was never made.
            sys.exit(0)

        else:
            # Check to see if there's a log in there where a transfer was made to a specific account.
            f = open("/home/.checker/responses/wire_logs.txt", "r")
            if ("271828182845" in f.read()):
                # A transfer to this account was made.
                sys.exit(1)

            else:
                # A transfer wasn't made to this specific account.
                sys.exit(0)

    # Step 19: Multiple choice question.
    elif (step == "19"):
        # Write the selection to a text file:
        f = open("/home/.checker/responses/step_19_answer.txt", "w+")
        f.write(query)
        f.close()

        # Printing the answers and return values:
        if (query == "A SELECT statement cannot be nested with a INSERT or UPDATE statement."):
            print("Multiple queries can be called together, no matter their behavior. They can be separated with semicolons, and it's still a valid SQL query.")
            sys.exit(0)

        elif (query == "The ID field restricts how many characters you can type. You would max out the character limit."):
            print("The ID field allows an unlimited amount of characters. However, not restricting the ID field is a security vulnerability, as well as allowing characters instead of just numbers.")
            sys.exit(0)

        elif (query == "INSERT or UPDATE provides no output. So, the statement(s) cannot be used."):
            print("Although INSERT and UPDATE return zero rows, it will still be a valid query. If such an attack worked, returning zero rows would likely produce a \"User Not Found\" error, but insertion/updating would still happen.")
            sys.exit(0)

        elif (query == "You cannot have more than one query when executing statements in FCCU.php."):
            print("When not using prepared statements, the mysqli_query() statement is being used. However, if you want to execute multiple queries within one statement, you need to use mysqli_multi_query().<br><br>Source: <a href=\"https://www.php.net/manual/en/mysqli.multi-query.php\">https://www.php.net/manual/en/mysqli.multi-query.php</a>")
            sys.exit(1)

    # Step 20: Fixing the vulnerability.
    elif (step == "20"):
        # Need to check multiple functions to see if the query statements are all fixed in FCCU.php.
        # Shouldn't happen, but first, make sure that the file exists.
        if (not os.path.exists("/usr/lib/cgi-bin/FCCU.php")):
            # File (somehow) doesn't exist. Exit with error.
            sys.exit(2)

        # Now, read in the file.
        f = open("/usr/lib/cgi-bin/FCCU.php")
        code = f.read()
        f.close()

        # Create the regex that will gather everything inside of the prepared statement comments.
        pattern = re.compile(r"(?<=/\*{3} Block #[1-9]: CONVERT TO PREPARED STATEMENT \*{3}\/)(.*?)(?=\/\*+\/)", re.DOTALL)

        # Find all matches. There should be 9 of these.
        matches = pattern.findall(code)
        if (len(matches) != 9):
            sys.exit(2)

        # Create an empty array, where each line in the matches will be added to them.
        lines_to_check = []

        # For each "block", split by new lines, then add the stripped line into the array.
        for match in matches:
            new_string = match.split('\n')
            for line in new_string:
                # Some strings will be empty. Skip adding those.
                if (line.strip() != ''):
                    lines_to_check.append(line.strip())

            # Adding a "divider" between each block. This will be used to help students know where their block failed at.
            lines_to_check.append("")

        # Now, performing the checks. These are the following functions that are required to be called in each block:
        required_statements = ["prepare", "bind_param", "execute", "get_result", "fetch_row"]
        # These count the number of times that each call above has been detected.
        required_counts = [0, 0, 0, 0, 0]

        # This is a regular expression to check if the line starts with a comment.
        comment_regex = re.compile(r"(^\/{2,}|^\/\*)")

        # This is going to be a counter, which will return the code block that the functions fails on.
        # This will tell the student where the checker fails at.
        counter = 1

        # For each line in the block:
        for line in lines_to_check:
            # If any of the lines contain the query call, mark as a fail. Return the counter, indicating the current block.
            if ("$mysqli->query" in line):
                print("$mysqli->query appeared in block #" + str(counter) + ". Please convert this block into a prepared statement.")
                sys.exit(0)

            # The end of the block was finished. Check to see if all functions were used.
            elif (line == ""):
                # Prepare an output string, in case any of the functions were missed. This will be given to the student.
                output = "Inside of block #" + str(counter) + ", "

                # A "for" loop to check if all required functions were used.
                function_index = 0
                for check_value in required_counts:
                    # If the check_value is zero, then that specific function was not found.
                    if (check_value == 0):
                        # Get the name of the function that wasn't used.
                        output += "\"" + required_statements[function_index] + "\" cannot be found. "
                    function_index += 1

                # Check if the output string was changed. If so, there was an error in the block. Exit after printing.
                if (output != "Inside of block #" + str(counter) + ", "):
                    print(output)
                    sys.exit(0)

                # Otherwise, continue onto the next block. Reset the counter values.
                required_counts = [0, 0, 0, 0, 0]
                counter += 1

            else:
                # For each element in the lines_to_check array, check if it includes any of the five functions above.
                # If that line starts with a comment, do not count it. The function must be uncommented.
                for function in required_statements:
                    if (re.search(comment_regex, line)):
                        # print("There was a comment! Skipping the function: " + line)
                        break

                    if (function in line and not (re.search(comment_regex, function))):
                        # Get the index of that function's name, then increment that index in required_counts.
                        index = required_statements.index(function)
                        required_counts[index] += 1

        # If the check made it through all of the blocks, we can finally try doing a final payload to see if the login screen is fixed.
        result = subprocess.run("/home/.checker/perform_attack.py cgi-bin/FCCU", shell=True, capture_output=True, text=True)

        print(result)
        if (result.returncode == 1):
            # Success!
            if ("Your ID number and password you entered do not match." in result.stdout):
                # Success!
                sys.exit(1)

            else:
                # Payload triggered a SQLi.
                sys.exit(3)

        elif (result.returncode == 0):
            # Failure. Return 5 for this, since an error occurred with testing the payload, but the SQL statements were fixed.
            sys.exit(4)

main()
