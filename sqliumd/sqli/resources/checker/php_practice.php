<?php
// Check if the form is submitted and student_id is was filled in.
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['student_id'])) {
    // This is the value of the 'student_id' name in the HTML form.
    // Since this is only accessible during a POST request, the $_POST variable is being used.
    $student_id = $_POST['student_id'];

    // Database connection parameters.
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "practice";

    // Create connection.
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Check connection. Shouldn't give an error, unless the database was named incorrectly.
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // First, this is the SQL query that is being called to the database.
    // String are concatenated in PHP with a "." in between them.
    $sql = "SELECT student_id, student_name, student_grade FROM students WHERE student_id = $student_id;";

    // Execute the query
    $conn->multi_query($sql);

    // Place the result inside of a PHP variable called $result.
    $result = $conn->store_result();

    // Before printing the results, print the SQL statement that was just processed.
    echo "<p><u>Your SQL statement:</u> SELECT student_id, student_name, student_grade FROM students WHERE student_id = <u>$student_id</u></p>";

    // Check if the query was successful.
    if ($result) {
        // If there are more than zero results in the SQL query...
        if ($result->num_rows > 0) {
            // First, print off the start of the table element. Do not close it yet.
            echo "<table border='1' style='margin-bottom: 10px;'>
                    <tr>
                        <th>Student ID</th>
                        <th>Student Name</th>
                        <th>Student Grade</th>
                    </tr>";

            // For each of the rows in the SQL query...
            // The "fetch_assoc" function turns the query into an array. It will iterate through each row.
            while ($row = $result->fetch_assoc()) {
                // Create an entry in the table.
                echo "<tr>
                        <td>{$row['student_id']}</td>
                        <td>{$row['student_name']}</td>
                        <td>{$row['student_grade']}</td>
                      </tr>";
            }
            // Once complete, close off the table.
            echo "</table>";
        }

        // If no results were found, then display that.
        else {
            echo "<p style='margin-bottom: 10px;'>No results found. Please enter a valid ID. <p>";
        }
    }

    // If no result could be retrieved, there was a SQL error. Display the error.
    else {
        echo "Error: " . $conn->error;
    }

    // Close the database connection
    $conn->close();
}

// If the student_id field was not entered or was never submitted, it will return an error.
else {
    echo "<p style='margin-bottom: 10px;'>Enter a valid student ID in the field below.</p>";
}
?>

<!-- This is for the HTML form. No need to change anything below. -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SQLi Practice</title>
</head>
<body>
    <form action="php_practice.php" method="post">
        <label for="student_id">Enter Student ID:</label>
        <input type="text" id="student_id" name="student_id">
        <input type="submit" value="Submit">
    </form>
</body>
</html>
