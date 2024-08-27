<?php
$server = "localhost";
$username   = "root";
$password   = "";
$database   = "forum";
 
if(!mysqli_connect($server, $username, $password, $database))
{
    exit("Error: could not establish database connection");
}

else {
    $link = mysqli_connect($server, $username, $password, $database);
}

?>