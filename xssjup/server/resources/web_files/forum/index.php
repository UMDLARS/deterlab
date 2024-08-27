<?php
//create_cat.php
require_once 'connect.php';
require_once 'header.php';
 
$sql = "SELECT
            cat_id,
            cat_name,
            cat_description
        FROM
            categories";
 
$result = mysqli_query($link, $sql);
 
if(!$result)
{
    echo "The categories could not be displayed, please try again later.";
}
else
{
    if(mysqli_num_rows($result) == 0)
    {
        echo "No categories defined yet.";
    }
    else
    {
        //prepare the table
        echo "<table border='1'>
              <tr>
                <th>Category</th>
                <th>Last topic</th>
              </tr>"; 

        while($row = mysqli_fetch_assoc($result))
        {
	    $sql = "SELECT * FROM topics WHERE topic_cat = " . $row["cat_id"] . " ORDER BY topic_date DESC";
	    $topics_result = mysqli_query($link, $sql);
	    $topics = mysqli_fetch_assoc($topics_result);
            echo "<tr>";
                echo "<td class='leftpart'>";
                    echo "<h3><a href='category.php?id=" . $row["cat_id"] . "'>" . $row["cat_name"] . "</a></h3>" . $row["cat_description"];
                echo "</td>";
                echo "<td class='rightpart'>";
		if (!$topics) {
                    echo "No topics yet";
		}
		else {
		    echo "<a href='topic.php?id=" . $topics["topic_id"] . "'>" . $topics["topic_subject"] . "</a> posted on " . $topics["topic_date"];
		}
		
                echo "</td>";
            echo "</tr>";
        }
    }
}
 
include 'footer.php';
?>
