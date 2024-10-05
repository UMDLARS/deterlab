#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    const char *hidden_file = "/usr/share/discover/dtd/.findme.txt";
    if (access(hidden_file, F_OK) == 0) {
        return 0;
    }
    else {
        return 1;
    }

    return 0;
}
