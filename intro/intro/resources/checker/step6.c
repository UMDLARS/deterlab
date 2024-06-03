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

    // Creating two variables: Path to sowpods.txt and path to output.txt.
    char path[128];
    char studentAns[128];
    snprintf(path, sizeof(path), "%s/sowpods.txt", homedir);

    // First, check to see if Important Data/ already exists. This step would've been previously passed.
    char imp_data[128];
    snprintf(imp_data, sizeof(imp_data), "%s/Important Data/", homedir);

    if (access(imp_data, F_OK) == 0) {
        // This will need to be converted into "Important\\ Data" after we call access on it,
        // since Unix requires escape characters when using spaces in directories.
        snprintf(studentAns, sizeof(studentAns), "%s/Important Data/output.txt", homedir);
    }

    else {
        snprintf(studentAns, sizeof(studentAns), "%s/output.txt/", homedir);
    }

    // Check to make sure that the sowpods.txt file exists.
    if (access(path, F_OK) == 0) {
        // File exists. Now, check if the student made an answer yet. 
        if (access(studentAns, F_OK) == 0) {
            // The answer exists, so we will generate a key.

            // Before generating a key, check to see if studentAns is in Important Data. If so, convert it to Unix format.
            if (strstr(studentAns, "Important Data") != NULL) {
                snprintf(studentAns, sizeof(studentAns), "%s/Important\\ Data/output.txt", homedir);
            }

            // Command buffer used for the following two checks. First, to create the key.
            char command[2048];
            snprintf(command, sizeof(command), "grep '^CAMP' %s > /tmp/.sowpods_camp_ans.txt", path);
            system(command);

            // Second, using diff to save the agony of writing C for file comparisons.
            snprintf(command, sizeof(command), "diff -q %s /tmp/.sowpods_camp_ans.txt", studentAns);
            int check = system(command);

            // Remove the file.
            system("rm -f /tmp/.sowpods_camp_ans.txt");

            // Check to see if the files were the same.
            if (check == 0) {
                // output.txt is correct.
                return 3;
            }
            else {
                // output.txt is different from the answer.
                return 4;
            }
        }
        else {
            // Answer doesn't exist.
            return 2;
        }
    }
    else { 
        // File doesn't exist.
        return 1;
    }

    // Check failed.
    return 0;
}
