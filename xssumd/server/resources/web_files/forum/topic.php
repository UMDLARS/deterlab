<?php
include 'connect.php';
include 'header.php';

$sql = "SELECT topic_subject FROM topics WHERE topic_id = " . mysqli_real_escape_string($link, $_GET['id']);
$result = mysqli_query($link, $sql);
if (!$result) {
  echo "Could not find topic.";
}
else {
  $row = mysqli_fetch_assoc($result);
  echo "<table border='1'>";
  echo "<tr><th colspan='2'>Replies for: " . $row['topic_subject'] . "</th></tr>";
  $sql = "SELECT 
	    posts.post_topic,
	    posts.post_content,
	    posts.post_date,
	    posts.post_by,
	    users.user_id,
	    users.user_name
 	  FROM posts LEFT JOIN users 
	  ON posts.post_by = users.user_id
	  WHERE posts.post_topic = " . mysqli_real_escape_string($link, $_GET['id']);
  $result = mysqli_query($link, $sql);
  if (!$result) {
    echo "<tr><td>No replies yet.</td></tr>";
  }
  else {
    while ($row = mysqli_fetch_assoc($result)) {
      echo "<tr>";
      echo "<td class='post-info'>";
      echo "Posted by:<br>";
      echo $row["user_name"] . "<br><br>";
      echo date('d-m-Y', strtotime($row['post_date']));
      echo "</td>";
      echo "<td class='post-content'>";
      echo $row["post_content"];
      echo "</td></tr>";
    }
  }
  echo "<tr><td colspan='2'>";
  echo "<form method='post' action='reply.php?id=" . mysqli_real_escape_string($link, $_GET['id']) . "'>";
  echo "  <textarea name='reply-content'></textarea>";
  echo "  <input type='submit' value='Submit Reply' />";
  echo "</form>";
  echo "</td></tr>";
}

include 'footer.php';
