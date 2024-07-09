#!/usr/bin/python3
import requests
import subprocess
import sys

# Function to execute the student's SQL queries and return results.
def execute_query(query):
    try:
        # Creating a connection and a cursor.
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='practice'
        )
        cursor = conn.cursor()

        # Take the provided query, then run it.
        cursor.execute(query)

        # Performing a SELECT statement, so fetch the results.
        result = cursor.fetchall()
        
        # There is no insertions/deletions, so no commit will be made.
        # Close the connection/cursor, then return the query result.
        conn.close()
        cursor.close()
        return result

    except mysql.connector.Error as e:
        print(f"Error executing SQL query: {e}")
        sys.exit(2)

def main():
    # Check to make sure that the function is called correctly.
    if (len(sys.argv) != 3):
        print("Usage: ./section_2.py <step_num> <query>")
        sys.exit(2)

    step = sys.argv[1]
    query = sys.argv[2]

    # First, make sure that the step number is between 12 and 14.
    if (int(step) >= 12 and int(step) <= 14):
        # Next, clear the database based on which step that the student is on.
        subprocess.run("/home/.checker/reset_db.py " + step, shell=True)

        # We are testing a SQLi payload for each step. Therefore, create a POST request.
        # Creating the URL for the php_practice.php file.
        url = 'http://localhost/php_practice.php'

        # Defining the payload
        data = {
            'student_id': query
        }

        # Send the POST request.
        response = requests.post(url, data=data)

        # Check if the request was successful.
        if (response.status_code == 200):
            # Take the response of the server, then write it to a file for the student's response.
            f = open("/home/.checker/responses/step_" + step + "_response.txt", "w+")

            # We only need up to the table, so we will remove the prompt, because it won't work in the notebook.
            # Just need to remove the HTML form, so we can split at the comment that is made.
            removed_prompt = (response.text).split("<!--")[0]
            f.write(removed_prompt)
            f.close()

            # Now, checking to see if the response is correct for the payload.
            expected_rows = []

            if (step == "12"):
                expected_rows = [
                    (100, 'Taylor', 'B'),
                    (101, 'Danny', 'B'),
                    (102, 'Hannah', 'D'),
                ]

            elif (step == "13"):
                expected_rows = [
                    (100, 'Taylor', 'B'),
                    (101, 'Danny', 'B'),
                    (102, 'Hannah', 'B'),
                ]

            elif (step == "14"):
                expected_rows = [
                    (100, 'Taylor', 'B'),
                    (101, 'Danny', 'B'),
                    (102, 'Hannah', 'B'),
                    (200, 'Jason', 'F')
                ]

            actual_results = execute_query("SELECT * FROM students")

            if (actual_results == expected_rows):
                sys.exit(1)

            else:
                sys.exit(0)
        
main()
