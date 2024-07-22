<?php
//create_cat.php
include 'header.php';
include 'connect.php';
include 'sanitize.php';

if (!isset($_SESSION['signed_in']) || $_SESSION['signed_in'] == false) {
    echo 'Sorry, you have to be <a href="signin.php">signed in</a> to create a category.';
}
else { 
  if($_SESSION['user_level'] != 1) {
    echo "You must have admin privileges to create a category.";
  }
  else {
    if($_SERVER['REQUEST_METHOD'] != 'POST') {
      //the form hasn't been posted yet, display it
      echo "<form method='post' action=''>
          Category name: <input type='text' name='cat_name' />
          Category description: <textarea name='cat_description' /></textarea>
          <input type='submit' value='Add category' />
        </form>";
    }
    else {
      //the form has been posted, so save it
      $sql = "INSERT INTO categories(cat_name, cat_description)
         VALUES('" . sanitize(mysqli_real_escape_string($link, $_POST['cat_name'])) . "',
               '" . sanitize(mysqli_real_escape_string($link, $_POST['cat_description'])) . "')";
      $result = mysqli_query($link, $sql);
      if(!$result) {
        //something went wrong, display the error
        echo "Error" . mysqli_error($link);
      }
      else {
        echo "New category successfully added.";
      }
    }
  }
}
?>
