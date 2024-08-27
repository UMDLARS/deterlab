#!/usr/bin/python3
import subprocess
import sys
import re
import os
import textwrap
import difflib

# This function will re-test the student's vulnerability to ensure it was patched.
def check_vulnerability(step):
    result = subprocess.run("/home/.checker/section_2.py " + step, shell=True)
    if (result.returncode == 1):
        return True

    else:
        return False

# This function will take two files for input, then return a list of the lines that are different.
def compare_files(file1_path, file2_path):
    # Open up both files at the same time.
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        # Create two lists, which contain each line of the files.
        file1_lines = file1.readlines()
        file2_lines = file2.readlines()

    # Finds the differences between the two files.
    diff = difflib.unified_diff(file1_lines, file2_lines, lineterm='')
    # Any file that has a +/- in front of it means it's different. Add it to the list.
    diff_list = [line for line in diff if line.startswith('+ ') or line.startswith('- ')]

    # For each of the elements, remove the first character (+/-), then trim it.
    for i in range(len(diff_list)):
        diff_list[i] = diff_list[i][1:].strip()

    # Return the list. Used in the main() function.
    return diff_list

def main():
    # Checks the usage. This shouldn't be giving an error, since it's called from the notebook.
    if (len(sys.argv) != 2):
        print("Usage: ./section_3.py <step_num>")
        sys.exit(2)

    step = sys.argv[1]

    # We need the student's username throughout this entire lab.
    with open('/etc/passwd') as f:
        for line in f:
            pass
        last_line = line
        username = last_line.split(":")[0]

    vulnerable = "/home/" + username + "/topic_2/step_" + str(int(step) - 4) + ".c"
    fix = "/home/" + username + "/topic_3/step_" + step + ".c"

    if (not os.path.exists(vulnerable) or not os.path.exists(fix)):
        sys.exit(4)

    # Much like section_2.py, this is going to be a lot of recycled code, but changes depending
    # on the step. First, compare the vulnerable file with the new one. The only difference
    # should be the function that got fixed.
    differences = compare_files(vulnerable, fix)

    # Creates a list of vulnerable functions with their fixes. Used to check the diff_list.
    functions = ["strcpy", "strncpy", "strcmp", "strncmp", "strcat", "strncat", "sprintf", "snprintf"]

    # Check if the difference list has a length of two. If so, we can check to see if the
    # student is using the available functions from the notebook.
    if (len(differences) == 2):
        # Create a list to store functions to be removed.
        functions_to_remove = []

        # Go through the functions list, and if they're in the diff list, mark them for removal.
        for function in functions:
            for diff_lines in differences:
                if function in diff_lines:
                    functions_to_remove.append(function)

        # Remove marked functions from the original list.
        for function in functions_to_remove:
            functions.remove(function)

        # Check to see if the length of the list is NOT equal to 6. If so, the function isn't patched correctly.
        if (len(functions) != 6):
            sys.exit(2)

    # The two files are the same.
    else:
        sys.exit(0)

    # Another check: Ensure that the previous function still fails.
    # The vulnerability is offsetted by four. step_13.c has its vulnerability in step_9.c, and so on.
    if (check_vulnerability(str(int(step) - 4))):
        # Step is passed. Test the student's patch. First, compile a temporary compiled file.
        temp_path = "/home/" + username + "/topic_3/"
        comp_result = subprocess.run("gcc -o " + temp_path + "/step_" + step + "_temp " + temp_path + "/step_" + step + ".c", shell=True)

        # Check if the compilation failed.
        if (comp_result.returncode != 0):
            sys.exit(3)

        # Run the file.
        result = subprocess.run(temp_path + "step_" + step + "_temp > /dev/null", shell=True)

        # Delete the temporary file.
        os.remove(temp_path + "step_" + step + "_temp")

        # Check to see if it succeeded.
        if (result.returncode == 0):
            # It succeeded. Now, we are going to copy the student's next payload into topic_3/.
            # If it's Step 16, the last step, create the Wormwood section if it's not created yet.
            if (step != "16"):
                src = "/home/" + username + "/topic_2/step_" + str(int(step) - 3) + ".c"
                dest = "/home/" + username + "/topic_3/step_" + str(int(step) + 1) + ".c"

                if (step != "16" and not os.path.exists(dest)):
                    subprocess.run("cp " + src + " " + dest, shell=True)

            # If the step is passed, but it's Step 16, we need to set up Wormwood.
            else:
                # Dependencies should've already been installed. Begin cloning.
                if (not os.path.exists("/home/" + username + "/topic_4/")):
                    subprocess.run('/home/.checker/create_topic_4.sh', shell=True)

            sys.exit(1)

    # Otherwise, the student vulnerable file doesn't pass the step. Should only happen if they changed their
    # original file.
    else:
        sys.exit(5)


main()
