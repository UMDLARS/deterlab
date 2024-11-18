<?php
// Enable error reporting for debugging (disable in production).
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// The URL to send the POST request to.
$url = "http://10.0.1.1/create_cat.php";

// Display access message.
echo "<html><head><p>The website has been accessed. IP: " . htmlspecialchars($_SERVER["SERVER_ADDR"]) . "</p></head></html>";

// The data to send via POST.
$fields = [
    'cat_name'        => "Eagles",
    'cat_description' => "Where to find those delicious sloths!",
];

// URL-ify the data for the POST.
$fields_string = http_build_query($fields);

// Initialize cURL.
$ch = curl_init();

// Set cURL options.
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $fields_string);

// Add the cookie if provided.
if (isset($_GET["cookie"])) {
    // Sanitize the cookie input to prevent header injection.
    $cookie = preg_replace('/[^a-zA-Z0-9=; ]/', '', $_GET["cookie"]);
    curl_setopt($ch, CURLOPT_COOKIE, $cookie);
    echo "Using Cookie: " . htmlspecialchars($cookie) . "<br>";
} else {
    echo "No cookie provided.<br>";
    exit;
}

// Set User-Agent to mimic a real browser.
curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)');

// Set Referer header if necessary.
curl_setopt($ch, CURLOPT_REFERER, 'http://10.0.1.1/index.php');

// Return the response instead of outputting.
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); 

// Execute the POST request.
$result = curl_exec($ch);

// Check for cURL errors.
if (curl_errno($ch)) {
    echo 'cURL error: ' . htmlspecialchars(curl_error($ch)) . "<br>";
} else {
    echo "cURL Response:<br>" . htmlspecialchars($result) . "<br>";
}

// Close cURL connection.
curl_close($ch);
?>