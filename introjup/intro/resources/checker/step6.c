#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <pwd.h>

int main() {
    // Ensure that sowpods.txt exists first.
    // Get the home directory.
    const char *homedir = getenv("HOME");

    if (homedir == NULL) {
        homedir = getpwuid(getuid())->pw_dir;
    }

    // Creating variables for paths to sowpods.txt and output.txt.
    char path[128];
    char studentAns[128];
    char studentAns_2[128];
    snprintf(path, sizeof(path), "%s/sowpods.txt", homedir);

    // Check if sowpods.txt exists in the home directory.
    if (access(path, F_OK) != 0) {
        // File doesn't exist.
        return 1;
    }

    // Now, construct the path(s) for output.txt directly in the home directory.
    snprintf(studentAns, sizeof(studentAns), "%s/output.txt", homedir);
    snprintf(studentAns_2, sizeof(studentAns_2), "%s/Important Data/output.txt", homedir);

    // Check if the student answer file exists.
    if (access(studentAns, F_OK) != 0) {
        // Answer file doesn't exist.
        // Before returning unsuccessful, check if it was moved from Step 7. If it did,
        // overwrite the path location.

        if (access(studentAns_2, F_OK) == 0) {
            // Exists, but was moved. Overwrite studentAns with this new path, then continue.
            // There's a space in "Important Data/", so quotes are surrounding it so that it works with diff.
            snprintf(studentAns, sizeof(studentAns), "\"%s\"", studentAns_2);
        }

        else {
            return 2;
        }
    }

    // Generate the key by searching for the lines that start with "CAMP" in sowpods.txt.
    char command[2048];
    snprintf(command, sizeof(command), "grep '^CAMP' %s > /tmp/.sowpods_camp_ans.txt", path);
    system(command);

    // Compare the generated key with the student's answer using diff.
    snprintf(command, sizeof(command), "diff -q %s /tmp/.sowpods_camp_ans.txt", studentAns);
    int check = system(command);

    // Remove the temporary file.
    system("rm -f /tmp/.sowpods_camp_ans.txt");

    // Check if the files were the same.
    if (check == 0) {
        // output.txt is correct.
        return 3;
    } else {
        // output.txt is different from the answer.
        return 4;
    }
}
