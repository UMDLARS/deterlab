#!/usr/bin/python3
import sys
import subprocess
import re
import os

# This function gets called whenever a specific routine gets ran.
def update_sanitize_routine(routine_number):
    file_path = "/var/www/html/sanitize.php"

    with open(file_path, 'r') as file:
        content = file.read()

    # Step 1: Comment out all routines
    comment_pattern = re.compile(r'(/\*\* Sanitize routine \d+ \*/\n)(/\*\*.*?\*/|function sanitize\(.*?\n\}\n)', re.DOTALL)
    all_routines = comment_pattern.findall(content)

    for routine in all_routines:
        body = routine[1]
        if not body.startswith('/**'):
            commented_body = f"/**\n{body}*/\n"
            content = content.replace(body, commented_body)

    # Step 1.5: Comment out the custom routine (routine 5)
    custom_pattern = re.compile(r'(\/\*+ Your Routine Here \*+\/\n)(/\*\*.*?\*\/|function sanitize\(.*?\n\}\n)(\/\*+)', re.DOTALL)
    custom_match = custom_pattern.search(content)

    if custom_match:
        body = custom_match.group(2)
        if not body.startswith('/**'):
            commented_body = f"/**\n{body}*/\n"
            content = content.replace(body, commented_body)

    # Step 2: Uncomment the specific routine.
    if routine_number != 5:
        uncomment_pattern = re.compile(rf'(/\*\* Sanitize routine {routine_number} \*/\n)/\*\*((.|\n)*?)\*/', re.DOTALL)
    else:
        uncomment_pattern = re.compile(r'(\/\*+ Your Routine Here \*+\/\n)/\*\*((.|\n)*?)\*/(\/\*+)', re.DOTALL)

    def uncomment_routine(match):
        header = match.group(1)
        body = match.group(2)
        footer = match.group(4) if routine_number == 5 else ''
        uncommented_body = body.strip()
        uncommented_body = re.sub(r'^\* ?', '', uncommented_body, flags=re.MULTILINE)
        return f"{header}{uncommented_body}\n{footer}"

    content = uncomment_pattern.sub(uncomment_routine, content)

    # Special handling to uncomment the custom routine if routine_number is 5
    if routine_number == 5:
        custom_uncomment_pattern = re.compile(r'(\/\*+ Your Routine Here \*+\/\n)\n?/\*\*(.*?\n)\*/\n?(\/\*+)', re.DOTALL)
        def handle_custom_uncomment(match):
            header = match.group(1)
            body = match.group(2)
            footer = match.group(3)
            uncommented_body = body.strip()
            uncommented_body = re.sub(r'^\* ?', '', uncommented_body, flags=re.MULTILINE)
            return f"{header}{uncommented_body}\n{footer}"
        content = custom_uncomment_pattern.sub(handle_custom_uncomment, content)

    # After updating the content, write the sanitize.php file with the updated code.
    with open(file_path, 'w') as file:
        file.write(content)

def main():
    # Checks if the file is being called correctly.
    if (len(sys.argv) != 3):
        print("Usage: ./section_4.py <step_num> <keep_work>")
        sys.exit(2)

    # Check if the step is between 2-4. If so, check if keep_work is 1 or 0. Otherwise,
    # if on Step 5, skip this check. It should be the victim's credit card number instead.
    if (sys.argv[2] != "1" and sys.argv[2] != "0"
         and int(sys.argv[1]) >= 7 and int(sys.argv[1]) <= 11):
        print("<keep_work> must be 1 (True) or 0 (False). If you are on Step 5, provide the victim's credit card number instead.")
        sys.exit(0)

    step = sys.argv[1]
    keep_work = sys.argv[2]

    # Forces NodeJS to run in 16.20.2, which is required for Puppeteer to work.
    os.environ['PATH'] = '/home/umdsectc/.nvm/versions/node/v16.20.2/bin:' + os.environ['PATH']

    # This is used for gathering the student's payload and the result from the home page.
    responses = []

    if (int(step) < 7 and int(step) > 11):
        print("Step must be between 7 and 11.")
        sys.exit[1]

    # If keep_work == 0, then we will have to test the entire website and see if XSS occurred.
    if (keep_work == "0"):
        # Create a call that will get a list of all the topic numbers.
        result = subprocess.run("mysql -uroot -e 'select topic_id from topics' forum | grep -e \"[0-9]\+\"", shell=True, capture_output=True, text=True)

        # Take the output of the command, split by newline, then remove the last element, since it's
        # just an empty string. The command above ends with a newline.
        topic_nums = ((result.stdout).split('\n'))[:-1]

        # Now, we will need to create a string of URLs with these topic numbers. These need
        # to be sent to section_4.js.
        urls = ""
        for i in topic_nums:
            urls += "http://10.0.1.1/topic.php?id=" + str(i) + " "

        # Next, start to check each step. The sanitize.php function will need to be altered at each step.
        # The (- 6) is to apply an offset. Step 7 is routine 1. Step 8 is routine 2, etc.
        routine = int(step) - 6
        update_sanitize_routine(routine)

        # Test the student's payload with the sanitization function.
        result = subprocess.run("node /home/.checker/section_4.js \'" + urls + "\'", shell=True, capture_output=True, text=True)

        # Each page is accessed. The JS file should've created a file that can be used to analyze.
        # Save the response.
        f = open("/home/.checker/responses/step_" + step + "_response.txt", "w+")
        f.write(result.stdout)
        f.close()

        # Since the response is stored as "result", we can process the data. Take the source code that has "steal.php"
        # inside of it, and split it from the response of the home page, which should have "Eagles" in it.
        responses = (result.stdout).split("\n-DIVIDER-\n")

    # Student wants to keep their work from a previous attempt.
    elif (keep_work == "1"):
        if (not os.path.exists("/home/.checker/responses/step_" + step + "_response.txt")):
            sys.exit(3)

        else:
            f = open("/home/.checker/responses/step_" + step + "_response.txt")
            result = f.read()
            f.close()

            # Since the response is stored as "result", we can process the data. Take the source code that has "steal.php"
            # inside of it, and split it from the response of the home page, which should have "Eagles" in it.
            responses = result.split("\n-DIVIDER-\n")

    else:
        # Something wrong happened.
        sys.exit(2)

    # If splitting only returned one result, then that means the response was "No response".
    if (len(responses) == 1):
        sys.exit(0)

    # All checks should be done now. Time to parse the results and see if the Eagles category was made.
    pattern = re.compile(f'<a href="category\.php\?id=[0-9]+">Eagles<\/a><\/h3>Where to find those delicious sloths!<\/td><td class="rightpart">')
    if (re.search(pattern, responses[1])):
        # Now, check to see if a payload was in the forum.
        # There should always be two responses after splitting from the divider.
        if ("steal.php" in responses[0]):
            # Should be a valid enough check to ensure that the payload worked.
            sys.exit(1)

        else:
            # No occurrence of steal.php means that there was no payload.
            sys.exit(0)

    # Eagles wasn't made, so exit with failure.
    else:
        sys.exit(0)

main()
