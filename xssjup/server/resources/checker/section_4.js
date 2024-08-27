#!/usr/bin/env node

// NOTE: "await" is used many times in this script. This means that it will wait until its called
// function is complete before it runs. Asynchronous calls are being made in this script, and to
// prevent race conditions, the await statement is made so that there are less errors that could
// "await" is called whenever page navigation, writing, or content is being rendered.

const puppeteer = require('puppeteer');
const fs = require('fs').promises;

// This is the "main" function that gets called.
async function run(urls) {
    // Create a browser and a page.
    const browser = await puppeteer.launch({
        headless: true,
        args: [
            '--disable-web-security',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-features=IsolateOrigins,site-per-process'
        ]
    });
    const page = await browser.newPage();

    // Step 1: Log in as root user
    await page.goto('http://10.0.1.1/signin.php', { waitUntil: 'networkidle2' });

    // Add a delay to ensure the page loads fully
    await new Promise(resolve => setTimeout(resolve, 2000));

    await page.type('#userfield', 'root');
    await page.type('#passfield', 'root');

    await page.click('#signin_button');

    // Step 2: Extract the PHPSESSID cookie
    const cookies = await page.cookies();
    const sessionCookie = cookies.find(cookie => cookie.name === 'PHPSESSID');

    // For debugging.
    // console.log('Extracted PHPSESSID cookie:', sessionCookie);

    // This function will only take one URL. This will be ran in a for loop.
    async function accessForum(url) {
        // If there's a request error (which there shouldn't), then print the reason.
        // This may affect the section_4.py script.
        /*
        page.on('requestfailed', request => {
            console.log(`${request.url()} failed to load. Reason: ${request.failure().errorText}`);
            console.log("Details:", request.headers(), request.postData());
        });
        */

        page.on('console', msg => {
            // console.log("Console log: " + msg.text());
        });

        try {
            // Accesses the webpage, assigns response. Wait until "networkidle2" means the function is
            // complete when no more than two calls are made within 500ms.
            // Start navigation to the URL

            const response = await page.goto(url, {
                waitUntil: 'networkidle0',
                timeout: 5000 // Time out after 5 seconds
            });

            // Check if the initial navigation was successful
            if (response.ok()) {
                // console.log("Successfully accessed " + url);

                // Capture the content of the final page
                const content = await page.content();

                return content;
            } else {
                console.log("Error accessing " + url);
                return "Error";
            }
        } catch (error) {
            console.log("Error accessing " + url + ": " + error.message);
            return "Error";
        }

    }

    // Create an empty string, where we will append page responses to it.
    var final_response = ""

    for (var i = 0; i < urls.length; ++i) {
        // First, this will actually ACCESS the page using the browser.
        const response = await accessForum(urls[i]);

        // If there's an error, it would be picked up here. Used for debugging.
        if (response.substring(0, 5) === "Error") {
//            console.log(response);
            break;
        }

        // Once the page is accessed, next, we would have to call a GET request. A working
        // payload in this lab will redirect the client. However, in order to check the
        // student's work, we will need a GET request to evaluate their payload. Used in the
        // section_4.py script that this JS file is called from.

        // Once the page is accessed, next, we would have to call a GET request.
        const get_response = await page.evaluate(async (url) => {
            const res = await fetch(url);
            const text = await res.text();
            return text;
        }, urls[i]);

        // If "steal.php" is in the response, then this is where a payload is detected.
        // Take the response and append it to the "final_response".
        if (get_response.includes("steal.php")) {
            final_response += get_response;
        }

    }

    // At the end, access the home page, get the response.
    // Check if Eagles was printed in the Python file. Create a divider to separate them.
    if (final_response !== "") {
        final_response += "\n-DIVIDER-\n";
        home_page_response = await accessForum("http://10.0.1.1/index.php");
        final_response += home_page_response;
    }

    else {
        final_response = "No response";
    }

    await browser.close();

    // This should be the only output in the end. Used in the Python script.
    console.log(final_response);
}

// Check if the usage is being called correctly.
if (process.argv.length != 3) {
    console.log("Usage: node ./section_4.js <list_of_urls>");
    process.exit(2);
}

// <list_of_urls> is a string. Convert into a list.
urls = process.argv[2].split(" ");

// There's a trailing space at the end, due to how the urls string was generated. Remove the empty
// URL. Otherwise, it will give an error, because there's a blank URL.
urls.pop()

// Run the "run" command above.
run(urls).catch(err => {
    console.error(err);
    process.exit(2);
});
