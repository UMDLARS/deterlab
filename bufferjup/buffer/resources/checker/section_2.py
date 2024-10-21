#!/usr/bin/python3
import subprocess
import sys
import re
import os
import textwrap

def main():
    # Checks the usage. This shouldn't be giving an error, since it's called from the noteboo>
    if (len(sys.argv) != 2):
        print("Usage: ./section_2.py <step_num>")
        sys.exit(2)

    step = sys.argv[1]

    # We need the student's username throughout this entire lab.
    username = "USERNAME_FOR_NODE"
    pathname = f"/home/{username}/topic_1"

    # Every step in this section is VERY similar to one another. No need for checking the individual steps.
    # Instead, of using if/else statements for each step, this is going to be a general check.
    # Checking for directory/file existence.
    if (not os.path.exists(pathname + "/step_" + step + ".c") or not os.path.exists(pathname + "/step_" + step)):
        sys.exit(2)

    # Before running this check, make sure that the function hasn't already been sanitized.
    f = open(pathname + "/step_" + step + ".c", "r")
    text = f.read()
    f.close()

    # Checking via regular expression. This depends on which step that the student is on.
    # Additionally, prepare the next file, depending on which step that the student is on.
    # Indentation gets really weird here. This is just so that it doesn't write the file so weird.
    if (step == "9"):
        pattern = r'\s*strcpy\(str2,\s*str1\);'
        next_file = """
#include <stdio.h>
#include <string.h>

void compare_string() {
    char str1[] = "Hello";
    char str2[] = "Hello";

    int result = strcmp(str1, str2);

    if (result == 0) {
        printf("The strings are the same!\\n");
    }

    else {
        printf("The strings are NOT the same!\\n");
    }
}

int main() {
    compare_string();
    return 0;
}
        """

    elif (step == "10"):
        pattern = r'\s*int\s*result\s*=\s*strcmp\(\s*str1,\s*str2\);'
        next_file = """
#include <stdio.h>
#include <string.h>

void concat_string() {
    char str1[20] = "Hello,";
    char *str2 = " World!\\n";

    strcat(str1, str2);

    printf("%s\\n", str1);
}

int main() {
    concat_string();
    return 0;
}
        """

    elif (step == "11"):
        pattern = r'\s*strcat\(str1,\s*str2\);'
        next_file = """
#include <stdio.h>

void sprintf_example() {
    char buffer[15];
    sprintf(buffer, "Hello, world!");
    printf("%s\\n", buffer);
}

int main() {
    sprintf_example();
    return 0;
}
        """

    # Step 12 has no next file.
    elif (step == "12"):
        pattern = r'\s*sprintf\(\s*buffer,\s*(?:\"|\')(.*)(?:\"|\')\s*\);'

    matches = re.findall(pattern, text, re.MULTILINE)

    # If there's a match, then proceed with checking.
    if (matches):
        # Compile the file as a temporary file.
        compile_result = subprocess.run("gcc -o " + pathname + "/step_" + step + "_temp " + pathname + "/step_" + step + ".c", shell=True, text=True, capture_output=True)

        # Check if it doesn't compile.
        if (compile_result.returncode != 0):
            os.remove(pathname + "/step_" + step + "_temp")
            sys.exit(3)

        # Run the file.
        result = subprocess.run(pathname + "/step_" + step + "_temp >/dev/null", shell=True, text=True, capture_output=True)

        # Delete the temp file.
        os.remove(pathname + "/step_" + step + "_temp")

        # Segmentation fault should occur.
        if (result.returncode == 139):
            # Create the next file for the student.
            if (not os.path.exists(pathname + "/step_" + str(int(step) + 1) + ".c") and step != "12"):
                # Remove leading whitespace and extra newline.
                next_file = textwrap.dedent(next_file).strip()

                f = open(pathname + "/step_" + str(int(step) + 1) + ".c", "w+")
                f.write(next_file)
                f.close()

            # Specific for Step 12.
            elif (step == "12"):
                # Create the new directory if it doesn't exist, then copy over Step 9.
                if (not os.path.exists("/home/" + username + "/topic_3")):
                    os.mkdir("/home/" + username + "/topic_3")

                # Check to see if step_13.c is made.
                if (not os.path.exists("/home/" + username + "/topic_3/step_13.c") and
                        os.path.exists(pathname + "/step_9.c")):
                    # Copy it over.
                    subprocess.run("cp " + pathname + "/step_9.c /home/" + username + "/topic_3/step_13.c", shell=True)

                # If step_9.c doesn't exist, then we have an error.
                elif (not os.path.exists(pathname + "/step_9.c")):
                    # Return special code.
                    sys.exit(5)

            # Now, exit.
            sys.exit(1)

	# No segmentation fault occurred.
        if (step != "10"):
            sys.exit(0)

        # Step 10 is a little different.
        if (step == "10"):
            # Need to check to make sure that the two strings are the same. Read in the file.
            f = open(pathname + "/step_10.c")
            text = f.read()
            f.close()

            pattern = r'\s*char\s*\w+\[\]\s*=\s*\{(.*)\};'
            matches = re.findall(pattern, text, re.MULTILINE)

            # There should be two matches, and they should be the same.
            if (len(matches) == 2):
                # Check if the two strings are the same, and if the result is 0 (not equal).
                if (matches[0] == matches[1] and result.returncode == 0):
                    # Success! But first, create the next file for the student..

                    if (not os.path.exists(pathname + "/step_11.c")):
                        # Remove leading whitespace and extra newline
                        next_file = textwrap.dedent(next_file).strip()

                        f = open(pathname + "/step_11.c", "w+")
                        f.write(next_file)
                        f.close()

                    # Now, exit successfully.
                    sys.exit(1)

                # Strings are not the same (as typed out in the variables).
                else:
                    sys.exit(0)

            # There must be two strings in order to match. If there are not two strings, then fail.
            else:
                sys.exit(0)

        # Otherwise, a failure.
        else:
            sys.exit(0)

    # No matches. Something must've been changed to the function's call.
    else:
        sys.exit(4)

main()
