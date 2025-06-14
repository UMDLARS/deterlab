#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

// Convert the student's SQL query to completely lowercase.
void to_lowercase(char* str) {
    for (int i = 0; str[i]; i++) {
        str[i] = tolower(str[i]);
    }
}

// A function to check the student's query, depending on the step that they are completing.
int check_query(const char* str, int step) {
    // All pre-configured to be lowercase. Case sensitivity doesn't matter in SQL, but does in C.
    // All checks will be done in lowercase, which is why the student's input needs to be lowercased before checking.
    const char* valid_queries[] = {
        "select * from students;",
        "select * from students where student_grade = 'a';",
        "select * from students where student_grade is not null;",
        "update students set student_grade = 'b' where student_name = 'aaron';",
        "delete from students where student_grade is null;",
        "select * from students limit 1 offset 1;"
    };

    // Adjust the index to match the step number.
    if (step >= 4 && step <= 9) {
        if (strcmp(str, valid_queries[step - 4]) == 0) {
            return 0;
        }
    }
    return 1;
}

int main(int argc, char* argv[]) {
    // Check if the correct number of arguments is provided.
    if (argc != 3) {
        printf("Usage: %s <step> <query>\n", argv[0]);
        return 2;  // Error code for incorrect usage.
    }

    // Extract the step number and the user's input.
    int step = atoi(argv[1]);
    char* input = argv[2];

    // Validate the step number.
    if (step < 4 || step > 9) {
        printf("Error: Step number must be between 4 and 9.\n");
        return 2;  // Error code for incorrect step number.
    }

    // Convert the input to lowercase.
    to_lowercase(input);

    // Check if the modified input matches any of the specified queries.
    int result = check_query(input, step);

    return result;
}
