#!/usr/bin/python3
import subprocess
import sys
import os
import re
import textwrap

def main():
    # Checks the usage. This shouldn't be giving an error, since it's called from the notebook.
    if (len(sys.argv) != 3):
        print("Usage: ./section_1.py <step_num> <answer (if step 6)>")
        sys.exit(2)

    step = sys.argv[1]

    # We need the student's username throughout this entire lab.
    with open('/etc/passwd') as f:
        for line in f:
            pass
        last_line = line
        username = last_line.split(":")[0]

    pathname = "/home/" + username + "/topic_1"

    # Checks Step 1.
    if (step == "1"):
        # Checking for directory/file existence.
        if (not os.path.exists(pathname + "/step_1.c")):
            sys.exit(2)

        # Source file exists. Compiling the program to see if it works.
        compile_result = subprocess.run('gcc -o ' + pathname + '/step_1 ' + pathname + '/step_1.c 2>/dev/null', shell=True)

        # Did not compile correctly.
        if (compile_result.returncode == 1):
            sys.exit(3)

        # If it gets to this point, then it did compile correctly.
        result = subprocess.run(pathname + '/step_1', shell=True, text=True, capture_output=True)

        # Delete the compiled file, since the student will be doing this in the next step.
        os.remove(pathname + "/step_1")

        # Checks if the username was printed.
        if (result.stdout == username + "\n" or result.stdout == username):
            sys.exit(1)

        # Checks to see if there was an error.
        elif (result.stderr != ""):
            sys.exit(3)

        # This is if there's no error, but did not print the username.
        else:
            sys.exit(0)

    # Check Step 2.
    elif (step == "2"):
        # Checking for file existence.
        if (not os.path.exists(pathname + "/step_2")):
            sys.exit(0)

        else:
            # Checking to make sure that it's not an empty file that the student may have created to "trick"
            # the notebook.
            result = subprocess.run('file ' + pathname + '/step_2', shell=True, text=True, capture_output=True)
            if ("step_2: ELF 64-bit LSB pie executable" in result.stdout):
                sys.exit(1)

            else:
                sys.exit(2)

    # Check Step 3.
    elif (step == "3"):
        # Checking for directory/file existence.
        if (not os.path.exists(pathname + "/step_2")):
            sys.exit(2)

        # Should be a fairly straight-forward process. This check is very similar to Step 1.
        result = subprocess.run(pathname + '/step_2', shell=True, text=True, capture_output=True)

        # Checks if the username was printed.
        if (result.stdout == username + "\n" or result.stdout == username):
            sys.exit(1)

        # Checks to see if there was an error.
        elif (result.stderr != ""):
            sys.exit(3)

        # This is if there's no error, but did not print the username.
        else:
            sys.exit(0)

    # Check Step 4.
    elif (step == "4"):
        # Checking for directory/file existence.
        if (not os.path.exists(pathname + "/step_4.c") or not os.path.exists(pathname + "/step_4")):
            sys.exit(2)

        # Before running the file, we will need to parse the text to see if the student followed directions.
        f = open(pathname + "/step_4.c", "r")
        text = f.read()
        f.close()

        # Two variables need to be created.
        # This regex will check if an uncommented line contains an int assignment between 1-1000.
        pattern = r'^\s*int\s+\w+\s*=\s*(?:[1-9]|[1-9][0-9]{1,2}|1000)\s*;$'

        # Find all matches.
        matches = re.findall(pattern, text, re.MULTILINE)

        # If there are exactly two matches, then it passes.
        if (len(matches) == 2):
            # Run the program, which should be between 1-2000. Silence output.
            result = subprocess.run(pathname + '/step_4 2>/dev/null', shell=True, text=True, capture_output=True)

            # In case there was an error.
            if (result.returncode == 1):
                sys.exit(3)

            # Convert to int. Need to cast, so wrap in a try/except block.
            try:
                output = int(result.stdout)

                if (output >= 2 and output <= 2000):
                    # Step is passed.
                    sys.exit(1)

                # Result was out of range.
                else:
                    sys.exit(0)

            except Exception as e:
                print(e)
                sys.exit(4)

    # Check Step 5.
    elif (step == "5"):
        # Checking for directory/file existence.
        if (not os.path.exists(pathname + "/step_5.c") or not os.path.exists(pathname + "/step_5")):
            sys.exit(2)

        # Before running the file, we will need to parse the text to see if the student followed directions.
        f = open(pathname + "/step_5.c", "r")
        text = f.read()
        f.close()

        # This regex pattern will check to see if a student created a variable without a comment in front.
        pattern = r'^\s*char\s+\w+(?:\[\])\s*=\s*\"(?:umdsec[a-z][a-z])\"\s*;$'

        # Find all matches.
        matches = re.findall(pattern, text, re.MULTILINE)

        # There should only be exactly one match.
        if (len(matches) == 1):
            # Extract the username.
            matched_username = re.findall(r'umdsec[a-z][a-z]', matches[0])

            # In case the username doesn't match the student.
            if (username != matched_username[0]):
                sys.exit(4)

            # Run the program, which should be "Hello, umdsecXX!". Silence any errors.
            result = subprocess.run(pathname + '/step_5 2>/dev/null', shell=True, text=True, capture_output=True)

            # In case there was an error.
            if (result.returncode == 1):
                sys.exit(3)

            # To add flexibility to the check, lowercase the output, then see if "hello, umdsecXX" is in the string.
            # This is in case the student decides not to include a '!'.
            output = (result.stdout).lower()

            if ("hello, " + username in output):
                sys.exit(1)

            else:
                sys.exit(0)

    # Check Step 6. This requires user input!
    elif (step == "6"):
        if (sys.argv[2] == "0"):
            # The answer is correct. Before exiting with code 1, we need to create a new file for the student for the next step.
            # If it already exists, do not overwrite it. This may lose progress if the student is checking all their answers.
            if (not os.path.exists(pathname + "/step_7.c")):
                # This is the source code for Step 7:
                step_7_outline = """
                #include <stdio.h>
    
                void sum(int* a, int* b, int* c) {
                    // Your answer here.
                }
    
                int main() {
                    int a, b, c;
    
                    a = 1;
                    b = 2;
                    c = 0;
    
                    // Your answer here.
    
                    printf("%d\n", c);
                    return 0;
                }
                """
    
                # Remove leading whitespace and extra newline
                step_7_outline = textwrap.dedent(step_7_outline).strip()
    
                f = open(pathname + "/step_7.c", "w+")
                f.write(step_7_outline)
                f.close()
    
            # Now, exit.
            sys.exit(1)

        else:
            sys.exit(0)

    # Checks Step 7.
    elif (step == "7"):
        # Checking for directory/file existence.
        if (not os.path.exists(pathname + "/step_7.c") or not os.path.exists(pathname + "/step_7")):
            sys.exit(2)

        # Before running the file, we will need to parse the text to see if the student followed directions.
        f = open(pathname + "/step_7.c", "r")
        text = f.read()
        f.close()

        # This regex pattern will check to see if the student has the correct answer inside of sum().
        pattern_1 = r'\*c\s*=\s*\*([ab])\s*\+\s*\*(?!\1)[ab]\s*;'

        # This regex pattern will check to see if the student called sum() correctly.
        pattern_2 = r'sum\s*\(\s*&a\s*,\s*&b\s*,\s*&c\s*\)\s*;'

        # Make sure that the answer is present before running.
        if re.search(pattern_1, text, re.MULTILINE) and re.search(pattern_2, text, re.MULTILINE):
            # Now, attempt to run the program. Silence any errors.
            result = subprocess.run(pathname + '/step_7 2>/dev/null', shell=True, text=True, capture_output=True)

            # In case there was an error.
            if (result.returncode == 1):
                sys.exit(3)

            # Remove the newline.
            answer = result.stdout[0]
            
            # Check to see if the output is 3.
            if (answer == "3"):
                # Before exiting successfully, create a new file for the next step.
                if (not os.path.exists(pathname + "/step_8.c")):
                    step_8_outline = """
                    #include <stdio.h>
                    #include <stdlib.h>

                    int main() {
                        // Create the variables.
                        int num_elements;
                        const float PI = 3.14159;

                        // Ask for user input.
                        printf("Enter the number of elements: ");
                        scanf("%d", &num_elements);

                        // TASK 1: Use malloc to create array_of_floats.
                        // It should be a pointer of type "float"!

                        // Populating the array.
                        for (int i = 0; i < num_elements; ++i) {
                            array_of_floats[i] = i * PI;
                        }

                        // Printing the elements.
                        printf("Array elements: ");
                        for (int i = 0; i < num_elements; ++i) {
                            printf("%.5f ", array_of_floats[i]);
                        }
                        printf("\\n");

                        // TASK 2: Free the array.

                        return 0;
                    }
                    """

                    # Remove leading whitespace and extra newline
                    step_8_outline = textwrap.dedent(step_8_outline).strip()

                    f = open(pathname + "/step_8.c", "w+")
                    f.write(step_8_outline)
                    f.close()

                # Now exit.
                sys.exit(1)

            else:
                sys.exit(0)

        # If both of the regular expressions don't pass, then the student doesn't have the correct answer.
        # This means they may have just set c = 3 to avoid answering the question properly.
        else:
            sys.exit(4)


    # Check Step 8.
    if (step == "8"):
        # Checking for directory/file existence.
        if (not os.path.exists(pathname + "/step_8.c") or not os.path.exists(pathname + "/step_8")):
            sys.exit(2)

        # Before running the file, we will need to parse the text to see if the student followed directions.
        f = open(pathname + "/step_8.c", "r")
        text = f.read()
        f.close()

        # This regex pattern will check to see if the student has the correct malloc statement.
        pattern_1 = r'\s*float\s*\*\s*array_of_floats\s*=\s*\(\s*float\s*\*\s*\)\s*malloc\s*\(\s*num_elements\s*\*\s*sizeof\s*\(\s*float\s*\)\s*\)\s*;'

        # This regex pattern will check to see if the student called free() correctly.
        pattern_2 = r'\s*free\(\s*array_of_floats\s*\);'

        # Make sure that the answer is present before running.
        if re.search(pattern_1, text, re.MULTILINE) and re.search(pattern_2, text, re.MULTILINE):
            # Now, attempt to run the program. Silence any errors.
            # Start the process.
            process = subprocess.Popen(pathname + '/step_8', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Send the input and get the output and error
            output, error = process.communicate(input="5\n".encode())

            # Decode the output and error
            output = output.decode()
            error = error.decode()

            # In case there was an error.
            if (error != ""):
                sys.exit(3)

            # Should be the correct output.
            if (output == "Enter the number of elements: Array elements: 0.00000 3.14159 6.28318 9.42477 12.56636 \n"):
                # Next step needs to be written before exiting.
                if (not os.path.exists("/home/" + username + "/topic_2/step_9.c")):
                    step_9_outline = """
                    #include <stdio.h>
                    #include <string.h>

                    void copy_string() {
                        char *str1 = "Hello!";
                        char str2[10];

                        strcpy(str2, str1);

                        printf("%s", str2);
                    }

                    int main() {
                        copy_string();
                        return 0;
                    }
                    """

                    # BEFORE WRITING, check if topic_2/ is created.
                    if (not os.path.exists("/home/" + username + "/topic_2/")):
                        os.mkdir("/home/" + username + "/topic_2/")

                    # Remove leading whitespace and extra newline
                    step_9_outline = textwrap.dedent(step_9_outline).strip()

                    f = open("/home/" + username + "/topic_2/step_9.c", "w+")
                    f.write(step_9_outline)
                    f.close()

                # Now exit.
                sys.exit(1)

            # Output is incorrect.
            else:
                sys.exit(0)

        # Either malloc or free were used incorrectly.
        else:
            sys.exit(4)

main()
