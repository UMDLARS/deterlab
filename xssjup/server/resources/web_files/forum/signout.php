<?php
session_start();
session_destroy();
include 'header.php';

echo 'You have successfully signed out. Return to the <a href="index.php">main menu</a>.';
?>
