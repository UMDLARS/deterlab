#!/usr/bin/python3
import sys
import subprocess
import mysql.connector
import re
import os

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

        # For SELECT queries, fetch all results.
        if query.strip().lower().startswith('select'):
            result = cursor.fetchall()
        else:
            result = None

        # In case there was an insertion/deletion, commit to save the changes.
        conn.commit()

        # Close the connection/cursor, then return the query result.
        conn.close()
        cursor.close()
        return result

    except mysql.connector.Error as e:
        # print(f"Error executing SQL query: {e}")
        sys.exit(2)

# Function to check if the database exists.
def check_database():
    try:
        result = subprocess.run('mysql -u root -e "SHOW DATABASES LIKE \'practice\';"', shell=True, capture_output=True, text=True)
        return "practice" in result.stdout
    except subprocess.CalledProcessError:
        return False

# Function to check if the table structure matches expectations.
def check_table_structure():
    result = subprocess.run("sudo mysql -u root -e \"DESCRIBE practice.students\" | grep student", shell=True, capture_output=True, text=True)

    # In case the database isn't created yet.
    if ("Table 'practice.students' doesn't exist\n" in result.stderr):
        sys.exit(3)

    # Create a list of the data values that are in the table. Last line is a blank line, so remove it.
    result = str(result.stdout).split("\n")[:-1]

    correctLines = [
        "student_id smallint(5) unsigned NO PRI NULL",
        "student_name varchar(64) YES NULL",
        "student_grade char(1) YES NULL"
    ]

    for line in result:
        # Strip extra whitespaces.
        output = re.sub(r'\s+', ' ', line)

        # Each line should be one of the following lines that were defined above.
        if (output.strip() not in correctLines):
            return False

    return True

# Function to verify inserted data.
# This check is going to be used for Step 4.
def verify_inserted_data():
    expected_rows = [
        (100, 'Aaron', 'A'),
        (101, 'Danny', 'B'),
        (102, 'Hannah', 'D'),
        (103, 'Abby', None)
    ]

    # If a student is running a "Calculate Grade" script, this step is going to fail because
    # the rows were changed in a future step. Their table structure will be saved, then checked
    # when "Calculate Grade" is clicked on.

    previously_passed = False
    if (os.path.exists("/home/.checker/responses/step_3_response.txt")):
        f = open("/home/.checker/responses/step_3_response.txt", "r")
        response = f.read()
        f.close()

        if (response == "[(100, 'Aaron', 'A'), (101, 'Danny', 'B'), (102, 'Hannah', 'D'), (103, 'Abby', None)]"):
            previously_passed = True

    try:
        # Retrieve and sort student data from the table.
        query = "SELECT student_id, student_name, student_grade FROM students ORDER BY student_id;"
        actual_rows = execute_query(query)

        # Write their response so that it can be checked later.
        if (actual_rows == expected_rows):
            f = open("/home/.checker/responses/step_3_response.txt", "w+")
            f.write(str(actual_rows))
            f.close()

        # Compare retrieved rows with expected rows.
        return (actual_rows == expected_rows) or previously_passed
    except:
        return False

# Main function to check each step.
def main():
    # Steps 1-3 can have <query> be anything. No query necessary for these answers.
    if len(sys.argv) != 3:
        print("Usage: ./section_1.py <step_num> <query>")
        sys.exit(2)

    step = sys.argv[1]
    user_query = sys.argv[2]

    # Step 1: Check if the database exists.
    if step == "1":
        if check_database():
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # Failure

    # Step 2: Check table structure.
    elif step == "2":
        if check_table_structure():
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # Failure

    # Step 3: Verify inserted data.
    elif step == "3":
        if verify_inserted_data():
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # Failure

    # Step 4-9: Checking SQL queries.
    elif step in ["4", "5", "6", "7", "8", "9"]:
        # Need to trim the user query first before running it through the C binary. There's no nice trim function in C.
        user_query = " ".join(user_query.split())
        user_query = re.sub(r'(?<=\S)\s*=\s*(?=\S)', ' = ', user_query)
        user_query = re.sub(r'\s+;', ';', user_query)
        
        result = subprocess.run("/home/.checker/check_sql " + step + " \"" + user_query + "\"", shell=True, capture_output=True, text=True)
        print(result)
        sys.exit(result.returncode)

    else:
        sys.exit(2)

main()
