// Some required variables for the phantomjs library.
var umdsec_url = "http://10.0.1.1/xss_practice.php?auth=W2awX7vJY4jQ4bMd9I964rMqvHvWz8Ox";
var victim_url = "http://10.0.1.1/xss_practice.php?auth=FaHyOnofllkfeD9D56ctAEtWBB4jTwrr";
var system = require('system');
var page = require('webpage').create();
var args = system.args;

// Required for writing files.
var fs = require('fs');

// This is the command if you are running it on the Docker container.
// If not running on the Docker container, use this command:
// Build first: sudo docker build -t section_2 .
// Then run: sudo docker run -v /home/.checker/responses:/output section_X <step_num>
if (args.length !== 2) {
    console.log('Usage: phantomjs section_2.js <step_num>');
    phantom.exit(0);
}

// The step number.
var step = args[1];

// Multiple websites need to be accessed in this script. Here's the template for it.
// user = umdsec_url is for accessing the umdsec account.
// user = victim_url is for accessing the Hacker account.
// phantomjs requires a callback instead of return values. We return the page content or "False".
function accessWebsite(user, callback) {
    page.open(user, function(status) {
        console.log("Status: " + status);
        if (status !== 'success') {
            callback("Error");
        }
        else {
            callback(page.content);
        }
    });
}

// Step 2:
if (step == 2) {
    // Message handler. Will be called when the page is opened.
    // This will print out the console.log output.
    page.onConsoleMessage = function(msg) {
        console.log(msg);
    };

    // Access the umdsec_url, then use the "content" variable and save the response.
    accessWebsite(umdsec_url, function(content) {
        // If the site couldn't be accessed, return 0. Check failed.
        if (content === "Error") {
            phantom.exit(0)
        }

        // If the site was accessed, we have a response. Need to write the response.
        else {
            // This section_2 is ran in a Docker container.
            // This will output into /output in the Docker container, but you must
            // mount the responses/ folder to the /output folder. View the example
            // run command above to know how to do this.
            var path = '/output/step_2_response.txt';
            try {
                fs.write(path, content, 'w');
                phantom.exit(1)
            }
            catch (e) {
                console.log("File write error: " + e);
                phantom.exit(2);
            }
        }
    });
}

// Step 3:
else if (step == 3) {
    // First, to check this step, access the victim's website and print the source code.
    var content = accessWebsite(victim_url);

    // Second, access the student's page to execute any JavaScript code, if any.
    var umdsec_content = accessWebsite(umdsec_url);

    // Third, access the victim's site again, obtain the source code. Needed for comparison next.
    var content_2 = accessWebsite(victim_url);

    // Before doing comparisons, check to see if any of the pages returned 404.
    if (content === "Error" || umdsec_content === "Error" || content_2 === "Error") {
        phantom.exit(2);
    }

    // Now, check to see if a new note was made between content and content_2.
    if (content !== content_2) {
        phantom.exit(1);
    }

    // If the two strings are the same, then the payload did not create a new note.
    else if (content === content_2) {
        phantom.exit(0);
    }

}
