#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pwd.h>
#include <sys/stat.h>
#include <sys/types.h>

// A C file is being used for Section 1, as it contains answers that would be
// visible to the students. When steps are finished, a finish_step_X() function
// is called, which writes out the "answer" or the next set of files.

// This must match the string in the Python file.
#define REQUIRED_SECRET "897dba53d0bd4e72adf9215db3948"

void finish_step_2() {
    // Get the home directory.
    const char *homedir = getenv("HOME");
    if (homedir == NULL) {
        homedir = getpwuid(getuid())->pw_dir;
    }

    // This is to create the templates directory within their home directory.
    char templates_dir[50];
    snprintf(templates_dir, sizeof(templates_dir), "%s/templates", homedir);
    mkdir(templates_dir, 0755);

    // Construct file path for the HTML file.
    char filepath[256];
    snprintf(filepath, sizeof(filepath), "%s/step_3.html", templates_dir);

    // Creating the file for the next step.
    FILE *file = fopen(filepath, "w");
    const char *html_content =
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head>\n"
        "    <title>Step 3 Demo</title>\n"
        "</head>\n"
        "<body>\n"
        "    <h1>Welcome to Step 3!</h1>\n"
        "    <p>Previously, you printed an HTML tag. Now, you're displaying an entire file.</p>\n"
        "</body>\n"
        "</html>\n";
    fprintf(file, "%s", html_content);
    fclose(file);
}

void finish_step_3() {
    // Create /lab if it doesn't exist.
    struct stat st = {0};
    if (stat("/lab", &st) == -1) {
        // Create the directory.
        if (mkdir("/lab", 0755) == 0) {
            FILE *file = fopen("/lab/memo.py", "w");
            mkdir("/lab/templates", 0755);

            // Basic starter code for /lab/memo.py.
            const char *python_code =
                "from flask import Flask, render_template, request, redirect, url_for, send_file, abort\n"
                "import os\n"
                "\n"
                "# For debugging:\n"
                "import sys\n"
                "\n"
                "app = Flask(__name__)\n"
                "MEMO_DIR = 'memos'\n"
                "\n"
                "os.makedirs(MEMO_DIR, exist_ok=True)\n"
                "\n"
                "@app.route('/')\n"
                "def index():\n"
                "    return render_template('index.html')\n"
                "\n"
                "@app.route('/add_memo', methods=['POST'])\n"
                "def add_memo():\n"
                "    # return (redirect to index())\n"
                "\n"
                "@app.route('/delete_memo/<int:memo_id>', methods=['POST'])\n"
                "def delete_memo(memo_id):\n"
                "    # return (redirect to index())\n"
                "\n"
                "@app.route('/memo/<path:memo_id>')\n"
                "def view_memo(memo_id):\n"
                "    return render_template('view_memo.html')\n";
            fprintf(file, "%s", python_code);
            fclose(file);

            // index.html
            FILE *file2 = fopen("/lab/templates/index.html", "w");
            const char *html_code_1 =
                "<!DOCTYPE html>\n"
                "<html>\n"
                "<head>\n"
                "    <title>Under Construction</title>\n"
                "</head>\n"
                "<body>\n"
                "    <h1>Website Under Construction</h1>\n"
                "    <p>We will be back shortly!</p>\n"
                "</body>\n"
                "</html>\n";
            fprintf(file2, "%s", html_code_1);
            fclose(file2);

            // view_memo.html
            FILE *file3 = fopen("/lab/templates/view_memo.html", "w");
            const char *html_code_2 =
                "<!DOCTYPE html>\n"
                "<html>\n"
                "<head>\n"
                "    <title>Under Construction</title>\n"
                "</head>\n"
                "<body>\n"
                "    <h1>Website Under Construction</h1>\n"
                "    <p>We will be back shortly!</p>\n"
                "</body>\n"
                "</html>\n";
            fprintf(file3, "%s", html_code_2);
            fclose(file3);

        } else {
            perror("mkdir");
        }
    }
}

void finish_step_4() {
    FILE *file1 = fopen("/lab/memo.py", "w");
    const char *python_code = "from flask import Flask, render_template, request, redirect, url_for, send_file, abort\n"
               "import os\n"
               "\n"
               "# For debugging:\n"
               "import sys\n"
               "\n"
               "app = Flask(__name__)\n"
               "MEMO_DIR = 'memos'\n"
               "\n"
               "os.makedirs(MEMO_DIR, exist_ok=True)\n"
               "\n"
               "@app.route('/')\n"
               "def index():\n"
               "    # Get the memos, sort them, then print index.html where \"memos\" is the list of memos.\n"
               "    memos = load_memos()\n"
               "    sorted_memos = dict(sorted(memos.items()))\n"
               "    return render_template('index.html', memos=sorted_memos)\n"
               "\n"
               "@app.route('/add_memo', methods=['POST'])\n"
               "def add_memo():\n"
               "    # Get the form with the name \"memo\", then get its content.\n"
               "    memo_content = request.form.get('memo')\n"
               "    # If it's not empty...\n"
               "    if memo_content:\n"
               "        # Get the next available memo ID and create a path with it.\n"
               "        memo_id = get_next_memo_id()\n"
               "        memo_filename = os.path.join(MEMO_DIR, str(memo_id))\n"
               "        # Create a file of the memo, and store it in memos/.\n"
               "        with open(memo_filename, 'w') as memo_file:\n"
               "            memo_file.write(memo_content)\n"
               "\n"
               "    # Redirect back to the index page.\n"
               "    return redirect(url_for('index'))\n"
               "\n"
               "@app.route('/delete_memo/<int:memo_id>', methods=['POST'])\n"
               "def delete_memo(memo_id):\n"
               "    # TO-DO: Add the functionality here for deleting files.\n"
               "\n"
               "    return redirect(url_for('index'))\n"
               "\n"
               "@app.route('/memo/<path:memo_id>')\n"
               "def view_memo(memo_id):\n"
               "    # Get the URL of the memo.\n"
               "    memo_filename = os.path.join(MEMO_DIR, str(memo_id))\n"
               "    memo_content = \"\"\n"
               "\n"
               "    # Attempt to access the file.\n"
               "    try:\n"
               "        # Read in the file as memo_content.\n"
               "        with open(memo_filename) as file:\n"
               "            memo_content = file.read()\n"
               "    except FileNotFoundError:\n"
               "        abort(404)\n"
               "\n"
               "    # Check if memo_id is numeric. If it's not, an error. Set memo_id = -1.\n"
               "    if not memo_id.isnumeric():\n"
               "        memo_id = -1\n"
               "\n"
               "    # Print view_memo.html page.\n"
               "    return render_template('view_memo.html', memo_id=memo_id, memo=memo_content)\n"
               "\n"
               "def load_memos():\n"
               "    memos = {}\n"
               "    for filename in os.listdir(MEMO_DIR):\n"
               "        with open(os.path.join(MEMO_DIR, filename), 'r') as memo_file:\n"
               "            memos[filename] = memo_file.read()\n"
               "    return memos\n"
               "\n"
               "def get_next_memo_id():\n"
               "    # Create a list of all the files in the memos/ directory.\n"
               "    filenames = os.listdir(MEMO_DIR)\n"
               "    # Create a list of the existing memos.\n"
               "    existing_ids = [int(filename) for filename in filenames if filename.isnumeric()]\n"
               "    # Get the maximum value, add one, then return it. This is the next memo id.\n"
               "    return max(existing_ids, default=0) + 1\n"
               "\n"
               "if __name__ == '__main__':\n"
               "    app.run(debug=True)\n";

    fprintf(file1, "%s", python_code);
    fclose(file1);

    // Creating the HTML for the view_memo.html template.
    FILE *file2 = fopen("/lab/templates/view_memo.html", "w");
    const char *html_code_1 =
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "    <meta charset=\"UTF-8\">\n"
        "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        "    <title>Memo {{ memo_id }}</title>\n"
        "</head>\n"
        "<body>\n"
        "    <h1>Memo {{ memo_id }}</h1>\n"
        "    <p>{{ memo }}</p>\n"
        "    <form action=\"{{ url_for('delete_memo', memo_id=memo_id) }}\" method=\"POST\">\n"
        "        <button type=\"submit\">Delete Memo</button>\n"
        "    </form>\n"
        "    <a href=\"{{ url_for('index') }}\">Back to memos</a>\n"
        "</body>\n"
        "</html>\n";
    fprintf(file2, "%s", html_code_1);
    fclose(file2);

    // Creating the HTML for the index.html template.
    FILE *file3 = fopen("/lab/templates/index.html", "w");
    const char *html_code_2 =
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "    <meta charset=\"UTF-8\">\n"
        "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        "    <title>Memos</title>\n"
        "</head>\n"
        "<body>\n"
        "    <h1>My Memos</h1>\n"
        "    <form action=\"{{ url_for('add_memo') }}\" method=\"POST\">\n"
        "        <textarea name=\"memo\" rows=5 style=\"width: 30%;\" placeholder=\"Enter memo here\"></textarea><br>\n"
        "        <button type=\"submit\">Add Memo</button>\n"
        "    </form>\n"
        "    <h2>Access Memos</h2>\n"
        "    <form>\n"
        "        <select onchange=\"window.location.href=this.value;\">\n"
        "            <option value=\"\">Select a memo</option>\n"
        "            {% for memo_id, memo in memos.items() %}\n"
        "                <option value=\"{{ url_for('view_memo', memo_id=memo_id) }}\">Memo {{ memo_id }}</option>\n"
        "            {% endfor %}\n"
        "        </select>\n"
        "    </form>\n"
        "</body>\n"
        "</html>\n";
    fprintf(file3, "%s", html_code_2);
    fclose(file3);
}

void finish_step_5() {
    FILE *file1 = fopen("/lab/memo.py", "w");
    const char *python_code = "from flask import Flask, render_template, request, redirect, url_for, send_file, abort\n"
               "import os\n"
               "\n"
               "# For debugging:\n"
               "import sys\n"
               "\n"
               "app = Flask(__name__)\n"
               "MEMO_DIR = 'memos'\n"
               "\n"
               "os.makedirs(MEMO_DIR, exist_ok=True)\n"
               "\n"
               "@app.route('/')\n"
               "def index():\n"
               "    # Get the memos, sort them, then print index.html where \"memos\" is the list of memos.\n"
               "    memos = load_memos()\n"
               "    sorted_memos = dict(sorted(memos.items()))\n"
               "    return render_template('index.html', memos=sorted_memos)\n"
               "\n"
               "@app.route('/add_memo', methods=['POST'])\n"
               "def add_memo():\n"
               "    # Get the form with the name \"memo\", then get its content.\n"
               "    memo_content = request.form.get('memo')\n"
               "    # If it's not empty...\n"
               "    if memo_content:\n"
               "        # Get the next available memo ID and create a path with it.\n"
               "        memo_id = get_next_memo_id()\n"
               "        memo_filename = os.path.join(MEMO_DIR, str(memo_id))\n"
               "        # Create a file of the memo, and store it in memos/.\n"
               "        with open(memo_filename, 'w') as memo_file:\n"
               "            memo_file.write(memo_content)\n"
               "\n"
               "    # Redirect back to the index page.\n"
               "    return redirect(url_for('index'))\n"
               "\n"
               "@app.route('/delete_memo/<int:memo_id>', methods=['POST'])\n"
               "def delete_memo(memo_id):\n"
               "    memo_filename = os.path.join(MEMO_DIR, str(memo_id))\n"
               "    if os.path.exists(memo_filename):\n"
               "        os.remove(memo_filename)\n"
               "    return redirect(url_for('index'))\n"
               "\n"
               "@app.route('/memo/<path:memo_id>')\n"
               "def view_memo(memo_id):\n"
               "    # Get the URL of the memo.\n"
               "    memo_filename = os.path.join(MEMO_DIR, str(memo_id))\n"
               "    memo_content = \"\"\n"
               "\n"
               "    ### Step 12 Solution START ###\n"
               "\n"
               "\n"
               "\n"
               "    ### Step 12 Solution END ###\n\n"
               "    # Attempt to access the file.\n"
               "    try:\n"
               "        # Read in the file as memo_content.\n"
               "        with open(memo_filename) as file:\n"
               "            memo_content = file.read()\n"
               "    except FileNotFoundError:\n"
               "        abort(404)\n"
               "\n"
               "    # Check if memo_id is numeric. If it's not, an error. Set memo_id = -1.\n"
               "    if not memo_id.isnumeric():\n"
               "        memo_id = -1\n"
               "\n"
               "    # Print view_memo.html page.\n"
               "    return render_template('view_memo.html', memo_id=memo_id, memo=memo_content)\n"
               "\n"
               "def load_memos():\n"
               "    memos = {}\n"
               "    for filename in os.listdir(MEMO_DIR):\n"
               "        with open(os.path.join(MEMO_DIR, filename), 'r') as memo_file:\n"
               "            memos[filename] = memo_file.read()\n"
               "    return memos\n"
               "\n"
               "def get_next_memo_id():\n"
               "    # Create a list of all the files in the memos/ directory.\n"
               "    filenames = os.listdir(MEMO_DIR)\n"
               "    # Create a list of the existing memos.\n"
               "    existing_ids = [int(filename) for filename in filenames if filename.isnumeric()]\n"
               "    # Get the maximum value, add one, then return it. This is the next memo id.\n"
               "    return max(existing_ids, default=0) + 1\n"
               "\n"
               "if __name__ == '__main__':\n"
               "    app.run(debug=True)\n";

    fprintf(file1, "%s", python_code);
    fclose(file1);
}

int main(int argc, char *argv[])
{
    // Checking the environment variable to make sure that the Python file is calling this file.
    const char* secret = getenv("CHECKER_SECRET");
    if (!secret || strcmp(secret, REQUIRED_SECRET) != 0) {
        fprintf(stderr, "Error: This program may only be run via section_1.py.\n");
        return 3;
    }

    // Checks the usage.
    if (argc != 2) {
        printf("Usage: ./section_1 <step_num>\n");
        return 2;
    }

    // Converts the argument into an int so that we can use it in the switch-case.
    int step = atoi(argv[1]);

    // All of the logic is being done in the Python program. We're just going to generate the next step.
    switch (step) {
        case 2:
            finish_step_2();
            return 0;
        case 3:
            finish_step_3();
            return 0;
        case 4:
            finish_step_4();
            return 0;
        case 5:
            finish_step_5();
            return 0;
        default:
            // Unrecognized step.
            return 1;
    }
}
