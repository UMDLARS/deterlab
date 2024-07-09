<?php
// Creating the database connection.
define('DB_SERVER', 'localhost');
define('DB_USERNAME', 'root');
define('DB_PASSWORD', '');
define('DB_NAME', 'xss');
 
// Attempt to connect to MySQL database.
$conn = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);

// Initialize the username variable to greet the user.
$username = "";

// Creating a variable for an authentication token.
$auth = "";

// If the "auth" variable is set, then this is you! Retrieving your username and your data.
// This is insecure! This is solely to help assist you, the student, learn how to steal data!
if (isset($_GET["auth"])) {
    // An authentication token is available! Identify the user.
    $auth = $_GET["auth"];

    // Creating the SQL statement and creating the prepared statement.
    $sql = "SELECT username FROM users WHERE auth = ?";
    $stmt = mysqli_prepare($conn, $sql);
    mysqli_stmt_bind_param($stmt, "s", $auth);
    mysqli_stmt_execute($stmt);

    // Get the username, then assign it to the variable.
    $result = mysqli_stmt_get_result($stmt);
    $row = mysqli_fetch_array($result);

    // Return the result.
    if (mysqli_num_rows($result) > 0) {
        $username = $row[0];
    }

    // No user exists.
    else {
        $username = "";
    }
}

// Before loading the site, check to see if a form is being submitted.
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // If the POST request is signing in.
    if (isset($_POST["username"]) && isset($_POST["password"])) {
        // In case the website needs to load while signing in...
        echo "Loading...";

        // Check to see if the username and password field have a match in the database.
        $username = $_POST["username"];
        $password = $_POST["password"];

        // Creating the SQL statement and creating the prepared statement.
        $sql = "SELECT * FROM users WHERE username = ? AND password = ?";
        $stmt = mysqli_prepare($conn, $sql);
        mysqli_stmt_bind_param($stmt, "ss", $username, $password);
        mysqli_stmt_execute($stmt);

        // Getting the results.
        $result = mysqli_stmt_get_result($stmt);
        $row = mysqli_fetch_array($result);

        // The third result from the $row variable is the authentication token, which will be used in the URL.
        header('location: ' . $_SERVER['PHP_SELF'] . "?auth=" . $row[2]);
    }

    // If the POST request is writing a note.
    else if (isset($_POST["note"]) && $_POST["note"] != "") {
        // Add the note to the database.
        $username = $_POST["username"];
        if ($username != "") {
            $sql = "INSERT INTO notes (username, note) VALUES (?, ?)";
            $stmt = mysqli_prepare($conn, $sql);
            mysqli_stmt_bind_param($stmt, "ss", $username, $_POST["note"]);
            mysqli_stmt_execute($stmt);
        }
        
        else {
            // Error.
            header("location: " . $_SERVER["REQUEST_URI"]);
        }
    }

    // If the POST request is a button that is used for demoing the lab.
    else if (isset($_POST["xss_action"]) && $_POST["xss_action"] != "") {
        // Check to see if we need to reset the notes for either the user or the victim.
        if ($_POST["xss_action"] == "Reset Your Notes" || $_POST["xss_action"] == "Reset Victim's Notes") {
            // Compose the SQL statement.
            $sql = "";

            if ($_POST["xss_action"] == "Reset Your Notes") {
                $sql .= "DELETE FROM notes WHERE username = 'umdsec'";
            }

            else if ($_POST["xss_action"] == "Reset Victim's Notes") {
                $sql .= "DELETE FROM notes WHERE username = 'Hacker'";
            }

            mysqli_query($conn, $sql);
        }

        // Otherwise, if we're "peeking", we will need to use a headless browser.
        // phantom.js is installed. We're going to call a script for that.
        shell_exec("phantomjs peek.js");
    }
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>XSS Practice</title>
</head>
<body>
    <?php
    // Checking to see if the user is signed in.
    if (isset($username) && $username != "") {
        echo '<p><strong>Welcome, ' . $username . '!</strong> Click <a href="xss_practice.php">here</a> to sign out.';

        // Creating a form to fill out a note.
        echo '
        <form action="' . $_SERVER["REQUEST_URI"] . '" method="post" id="noteForm">
            <label for="note">Post a custom note here:</label><br>
            <textarea rows="8" cols="50" id="note" name="note" form="noteForm" maxlength="1000"></textarea><br>
            <input type="hidden" name="username" value="' . $username . '">
            <input type="submit" value="Submit Note">
        </form>
        ';

        // Additionally, these buttons are used for resetting certain parts of the lab:
        echo '
        <p><em>Some additional buttons for the lab:</em></p>
        <form action="' . $_SERVER["REQUEST_URI"] . '" method="post">
            <input type="submit" name="xss_action" value="Reset Your Notes">
            <input type="submit" name="xss_action" value="Peek as Victim">
            <input type="submit" name="xss_action" value="Reset Victim\'s Notes">
        </form>
        ';

        // The user is signed in. Now, we can print their notes.
        $sql = "SELECT note FROM notes WHERE username = ?";
        $stmt = mysqli_prepare($conn, $sql);
        mysqli_stmt_bind_param($stmt, "s", $username);
        mysqli_stmt_execute($stmt);

        // Getting the result.
        $result = mysqli_stmt_get_result($stmt);

        // Checks to see if no rows are produced.
        if (mysqli_num_rows($result) == 0) {
            echo "<p><strong>You do not have any notes.</strong> Feel free to write one below!</p>";
        }

        else {
            echo '<hl>';
            echo '<h3>These are your current notes:</h3>';
            // Printing the notes. We will need a counter for this.
            $counter = 1;
            while ($row = mysqli_fetch_array($result)) {
                echo '<p>Note #' . $counter . ": " . $row[0];
                ++$counter;
            }
        }
    }

    // If not signed in, create a sign-in form.
    else {
        echo '<p>Welcome! You are not signed in.';
        echo '
        <form action="xss_practice.php" method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required><br><br>

            <label for="password">Password:</label>
            <input type="text" id="password" name="password" required><br><br>

            <input type="submit" value="Sign In">
        </form>
        ';
    }
    ?>

</body>
</html>