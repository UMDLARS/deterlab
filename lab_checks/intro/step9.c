#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <pwd.h>

int main() {
    // Get the home directory.
    const char *homedir = getenv("HOME");

    if (homedir == NULL) {
        homedir = getpwuid(getuid())->pw_dir;
    }

    // Creating two variables: Path to sowpods.txt and path to output.txt.
    char key[128];
    char studentAns[128];

    snprintf(key, sizeof(key), "/tmp/.step9Ans");
    snprintf(studentAns, sizeof(studentAns), "%s/Important Data/lists/listdiff.txt", homedir);

    if (access(studentAns, F_OK) == 0) {
        // The answer exists, so we will generate a key.

        // Command buffer used for the following two checks. First, to create the key.
        char command[2048];
        snprintf(command, sizeof(command), "diff \"%s/Important Data/lists/list1.txt\" \"%s/Important Data/lists/list2.txt\" > \"%s\"", homedir, homedir, key);
        system(command);

        // Second, using diff to save the agony of writing C for file comparisons.
        snprintf(command, sizeof(command), "diff -q \"%s\" %s > /dev/null", studentAns, key);
        int check = system(command);
        printf(command);

        // Remove the file.
        snprintf(command, sizeof(command), "rm -f %s", key);
        system(command);

        // Check to see if the files were the same.
        if (check == 0) {
            // output.txt is correct.
            return 1;
        }
        else {
            // output.txt is different from the answer.
            return 2;
        }
    }
    else {
        // Answer doesn't exist.
        return 3;
    }

    // Error with checking.
    return 0;
}
