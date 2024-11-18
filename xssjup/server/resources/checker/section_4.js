#!/usr/bin/env node

const puppeteer = require('puppeteer');
const fs = require('fs').promises;

// Main function
async function run(urls) {
    // Launch browser
    const browser = await puppeteer.launch({
        headless: true, // Set to false for debugging
        args: [
            '--disable-web-security',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-features=IsolateOrigins,site-per-process'
        ]
    });
    const page = await browser.newPage();

    // Enhanced logging
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('response', async response => {
//        console.log(`Response: ${response.status()} ${response.url()}`);

        // Check if the response URL starts with 'http://10.0.1.3'
        if (response.url().startsWith('http://10.0.1.3')) {
            try {
                // Attempt to get the response body as text
                const responseBody = await response.text();
//                console.log(`Response Body for ${response.url()}:\n${responseBody}`);
            } catch (error) {
//                console.log(`Failed to get response body for ${response.url()}: ${error}`);
            }
        }
    });

    // Listen for request failures
    page.on('requestfailed', request => {
//        console.log(`${request.url()} failed to load. Reason: ${request.failure().errorText}`);
//        console.log("Details:", request.headers(), request.postData());
    });

    // Additional console logging from the page
    page.on('console', msg => {
//        console.log("Console log:", msg.text());
    });

    try {
        // Step 1: Log in as root user
//        console.log('Navigating to sign-in page...');
        await page.goto('http://10.0.1.1/signin.php', { waitUntil: 'networkidle2' });

        // Add a delay to ensure the page loads fully
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Enter username and password
//        console.log('Entering credentials...');
        await page.type('#userfield', 'root', { delay: 100 });
        await page.type('#passfield', 'root', { delay: 100 });

        // Click the sign-in button and wait for navigation
//        console.log('Submitting login form...');
        await Promise.all([
            page.click('#signin_button'),
            page.waitForNavigation({ waitUntil: 'networkidle0' }),
        ]);

        // Step 2: Extract all relevant cookies
        const cookies = await page.cookies();
        const cookieString = cookies.map(cookie => `${cookie.name}=${cookie.value}`).join('; ');
//        console.log('Extracted Cookies:', cookieString);

        // Step 3: Access each URL sequentially
        let final_response = "";

        for (let i = 0; i < urls.length; ++i) {
            const currentUrl = urls[i];
//            console.log(`\nAccessing URL ${i + 1}: ${currentUrl}`);

            try {
                // Navigate to the current URL
                const response = await page.goto(currentUrl, { waitUntil: 'networkidle0', timeout: 30000 });

                if (response && response.ok()) {
//                    console.log(`Successfully accessed ${currentUrl}`);
                } else {
//                    console.warn(`Warning: Received status ${response.status()} for ${currentUrl}`);
                    final_response += `Error accessing ${currentUrl}: Status ${response.status()}\n`;
                    continue; // Skip to the next URL
                }
            } catch (error) {
//                console.error(`Error accessing ${currentUrl}: ${error.message}`);
                final_response += `Error accessing ${currentUrl}: ${error.message}\n`;
                continue; // Skip to the next URL
            }

            // Execute fetch within the page context to trigger 'steal.php'
            const get_response = await page.evaluate(async (url) => {
                try {
                    const res = await fetch(url, {
                        credentials: 'include' // Ensure cookies are sent with the request
                    });
                    return await res.text();
                } catch (e) {
                    return `Fetch error: ${e.message}`;
                }
            }, currentUrl);

            // Check if 'steal.php' was triggered
            if (get_response.includes("steal.php")) {
                final_response += get_response;
            } else {
//                console.log(`No 'steal.php' triggered for ${currentUrl}`);
            }
        }

        // Final Step: Access the home page and append its response if any 'steal.php' was triggered
        if (final_response !== "") {
            final_response += "\n-DIVIDER-\n";
//            console.log('\nAccessing home page...');
            const homePageResponse = await page.goto("http://10.0.1.1/index.php", { waitUntil: 'networkidle0', timeout: 30000 });

            if (homePageResponse && homePageResponse.ok()) {
                const homeContent = await page.content();
                final_response += homeContent;
//                console.log('Home page accessed successfully.');
            } else {
//                console.warn('Warning: Failed to access home page.');
                final_response += "Error accessing home page.\n";
            }
        } else {
            final_response = "No response from 'steal.php'.";
        }

        // Close the browser
        await browser.close();

        // Output the final response for use in the Python script
        console.log('\nFinal Response:\n', final_response);
    } catch (err) {
        console.error('An unexpected error occurred:', err);
        await browser.close();
        process.exit(2);
    }
}

// Ensure correct usage
if (process.argv.length !== 3) {
    console.log("Usage: node ./section_4.js '<list_of_urls>'");
    console.log("Example: node ./section_4.js 'http://10.0.1.1/topic.php?id=1 http://10.0.1.1/topic.php?id=2 http://10.0.1.1/topic.php?id=3'");
    process.exit(2);
}

// Convert the list of URLs from a space-separated string to an array
let urls = process.argv[2].split(" ").filter(url => url.trim() !== "");

// Execute the main function
run(urls).catch(err => {
    console.error('Script failed:', err);
    process.exit(2);
});
