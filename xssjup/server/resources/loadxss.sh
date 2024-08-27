#!/bin/bash

# Define the temporary directory and current user variables.
export TMP="/tmp/load"
export USER=$(whoami)

# Create the temporary directory if it doesn't exist.
mkdir -p $TMP

# Change to the temporary directory.
pushd $TMP

# Move the tarball into the temporary directory.
mv /tmp/${USER}_xss.tar.gz $TMP

# Extract the tarball while preserving permissions and ownerships.
sudo tar -xvpzf ${USER}_xss.tar.gz

# Check and move the sanitize.php file.
if [ -f "${TMP}/var/www/html/sanitize.php" ]; then
    sudo mv "${TMP}/var/www/html/sanitize.php" "/var/www/html/"
fi

# Check and move the responses directory, overwriting if it exists.
if [ -d "${TMP}/home/.checker/responses" ]; then
    sudo rm -rf "/home/.checker/responses"
    sudo mv "${TMP}/home/.checker/responses" "/home/.checker/"
fi

# Check and move the section_2.js file.
if [ -f "${TMP}/home/.checker/section_2.js" ]; then
    sudo mv "${TMP}/home/.checker/section_2.js" "/home/.checker/"
fi

# Check and move the section_2.py file.
if [ -f "${TMP}/home/.checker/section_2.py" ]; then
    sudo mv "${TMP}/home/.checker/section_2.py" "/home/.checker/"
fi

# Check and restore the database backup.
if [ -f "${TMP}/tmp/save/db_backup.sql" ]; then
    sudo mysql < "${TMP}/tmp/save/db_backup.sql"
fi

# Check if step_1_answer.txt exists and update the database.
if [ -f "/home/.checker/responses/step_1_answer.txt" ]; then
    auth=$(cat /home/.checker/responses/step_1_answer.txt)
    sudo mysql -e "UPDATE users SET auth = '$auth' WHERE username = 'umdsec';"
fi

# Check if step_5_answer.txt exists and update the database.
if [ -f "/home/.checker/responses/step_5_answer.txt" ]; then
    note=$(cat /home/.checker/responses/step_5_answer.txt)
    sudo mysql -e "UPDATE notes SET note = 'Credit card number to purchase the company some new merch: $note' WHERE username = 'hacker' AND note LIKE '%Credit%';"
fi

# Return to the previous directory.
popd

# Clean up.
# sudo rm -rf $TMP