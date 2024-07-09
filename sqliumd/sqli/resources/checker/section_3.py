#!/usr/bin/python3
import os
import sys
import subprocess
import mysql.connector

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
    if (len(sys.argv) != 1):
        print("Usage: ./section_3.py")
        sys.exit(1)

    # Only need to check Step 15 in this section.
    # First, attempt to get the path of the php_practice.php file.
    if (os.path.exists("/var/www/html/php_practice.php")):
        # File exists. Store the source code inside of a variable.
        f = open("/var/www/html/php_practice.php", "r")
        sourceCode = f.readlines()
        f.close()
        # Going through each line, get the lines that contain any mysqli statements.
        mysqli_statements = []
        for line in sourceCode:
            # If the line contains "sql" and is not a comment, then add it to the "checks".
            if ("sql" in line and "//" not in line):
                mysqli_statements.append(line.strip())

        # Now, we need to loop through all of the mysqli statements and check to make sure that
        # a proper prepared statement exists in the PHP file.

        # Create an array of strings that contains the required functions for prepared statements.
        # Will not check to see if $sql has a "?" in it. A SQLi attack will occur later, and if
        # "?" isn't in $sql, then the test will fail. Only checking to see if the required statements
        # are used.
        required_stmt = ["prepare", "bind_param", "execute", "get_result"]

        # Check all lines in the "required statements" array.
        for line in mysqli_statements:
            # Iterate through the required statements to see if it exists. If so, delete it from the array.
            for stmt in required_stmt:
                if (stmt in line):
                    required_stmt.remove(stmt)

        # If all required statements exist in the file, the length of the array should be zero.
        if (len(required_stmt) == 0):
            # Now, perform a SQLi attack.
            result = subprocess.run("/home/.checker/perform_attack.py php_practice", shell=True, capture_output=True, text=True)
            attack_output = result.stdout
            # Check the result's output and see if it printed every row from the table.
            db_result = execute_query("SELECT * FROM students")
            # Perform a loop to check to see if each element in the database was printed in the table.
            # Only going to check the names.
            for row in db_result:
                # If anyone's name appears, then it's a failed check.
                if (row[1] in result.stdout):
                    # Failure. Return 0.
                    sys.exit(0)

            # If the for loop passed, then return 1.
            sys.exit(1)

        # Not all required statements are being used.
        else:
            sys.exit(3)

    # Cannot find php_practice.php.
    else:
        sys.exit(2)

main()
