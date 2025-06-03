#!/usr/bin/python3
import subprocess
import sys
import mysql.connector

def main():
    if (len(sys.argv) != 3):
        print("Usage: ./section_1.py <step_num> <input>")
        sys.exit(1)

    step = sys.argv[1]
    input = sys.argv[2]

    # This section only has one step, so the step_num should be one.
    if (step == "1"):
        # Supposed to check if the input matches the authentication token
        # of the umdsec account. Checking the database.

        try:
            # Creating a connection and a cursor.
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='xss'
            )
            cursor = conn.cursor()

            # Take the provided query, then run it.
            cursor.execute("SELECT * FROM users WHERE auth = %s", [input])

            # Retrieve the result.
            result = cursor.fetchall()

            # Get the one and only result, then get the first element from it (username).
            if (len(result) == 1 and result[0][0] == "umdsec"):
                sys.exit(0)

            else:
                sys.exit(1)

        except mysql.connector.Error as e:
            print(f"Error executing SQL query: {e}")
            sys.exit(2)

main()
