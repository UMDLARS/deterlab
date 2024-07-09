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

main()
