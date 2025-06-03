#!/usr/bin/python3
import subprocess
import mysql.connector
import sys

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

        # Split the query into individual statements and execute them one by one.
        statements = query.split(';')
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)

        # In case there was an insertion/deletion, commit to save the changes.
        conn.commit()

        # Close the connection/cursor, then return the query result.
        conn.close()
        cursor.close()
        sys.exit(0)

    except mysql.connector.Error as e:
        print(f"Error executing SQL query: {e}")
        sys.exit(2)

def main():
    if (len(sys.argv) != 2):
        print("Usage: ./reset_db.py <step_num>")
        sys.exit(1)

    else:
        step_num = int(sys.argv[1])
        if (step_num >= 4 and step_num <= 15):
            # Including Step 7, in case the UPDATE command broke the student's table. Reverts them back to Step 6.
            if (step_num >= 4 and step_num <= 7):
                query = """
                DROP TABLE students;
                CREATE TABLE students (student_id SMALLINT UNSIGNED PRIMARY KEY,
                                       student_name VARCHAR(64),
                                       student_grade CHAR(1));
                INSERT INTO students (student_id, student_name, student_grade) VALUES (100, "Aaron", "A");
                INSERT INTO students (student_id, student_name, student_grade) VALUES (101, "Danny", "B");
                INSERT INTO students (student_id, student_name, student_grade) VALUES (102, "Hannah", "D");
                INSERT INTO students (student_id, student_name, student_grade) VALUES (103, "Abby", NULL);
                """
                execute_query(query)

            elif (step_num == 8):
                query = """
                DROP TABLE students;
                CREATE TABLE students (student_id SMALLINT UNSIGNED PRIMARY KEY,
                                       student_name VARCHAR(64),
                                       student_grade CHAR(1));
                INSERT INTO students (student_id, student_name, student_grade) VALUES (100, "Aaron", "B");
                INSERT INTO students (student_id, student_name, student_grade) VALUES (101, "Danny", "B");
                INSERT INTO students (student_id, student_name, student_grade) VALUES (102, "Hannah", "D");
                INSERT INTO students (student_id, student_name, student_grade) VALUES (103, "Abby", NULL);
                """
                execute_query(query)

            elif (step_num == 9 or step_num == 12):
                query = """
                DROP TABLE students;
                CREATE TABLE students (student_id SMALLINT UNSIGNED PRIMARY KEY,
                                       student_name VARCHAR(64),
                                       student_grade CHAR(1));
                INSERT INTO students (student_id, student_name, student_grade) VALUES (100, "Aaron", "B");
                INSERT INTO students (student_id, student_name, student_grade) VALUES (101, "Danny", "B");
                INSERT INTO students (student_id, student_name, student_grade) VALUES (102, "Hannah", "D");
                """
                execute_query(query)

            elif (step_num == 13):
                query = """
                DROP TABLE students;
                CREATE TABLE students (student_id SMALLINT UNSIGNED PRIMARY KEY,
                                       student_name VARCHAR(64),
                                       student_grade CHAR(1));
                INSERT INTO students (student_id, student_name, student_grade) VALUES (100, "Taylor", "B");
                INSERT INTO students (student_id, student_name, student_grade) VALUES (101, "Danny", "B");
                INSERT INTO students (student_id, student_name, student_grade) VALUES (102, "Hannah", "D");
                """
                execute_query(query)

            elif (step_num == 14):
                query = """
                DROP TABLE students;
                CREATE TABLE students (student_id SMALLINT UNSIGNED PRIMARY KEY,
                                       student_name VARCHAR(64),
                                       student_grade CHAR(1));
                INSERT INTO students (student_id, student_name, student_grade) VALUES (100, "Taylor", "B");
                INSERT INTO students (student_id, student_name, student_grade) VALUES (101, "Danny", "B");
                INSERT INTO students (student_id, student_name, student_grade) VALUES (102, "Hannah", "B");
                """
                execute_query(query)

            elif (step_num == 15):
                query = """
                DROP TABLE students;
                CREATE TABLE students (student_id SMALLINT UNSIGNED PRIMARY KEY,
                                       student_name VARCHAR(64),
                                       student_grade CHAR(1));
                INSERT INTO students (student_id, student_name, student_grade) VALUES (100, "Taylor", "B");
                INSERT INTO students (student_id, student_name, student_grade) VALUES (101, "Danny", "B");
                INSERT INTO students (student_id, student_name, student_grade) VALUES (102, "Hannah", "B");
                INSERT INTO students (student_id, student_name, student_grade) VALUES (200, "Jason", "F");
                """
                execute_query(query)

            else:
                sys.exit(1)

        else:
            sys.exit(1)

main()
