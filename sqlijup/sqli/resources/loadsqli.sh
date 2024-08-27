#!/bin/bash

# Define the temporary directory and current user variables.
export TMP="/tmp/load"
export USER=$(whoami)

# Create the temporary directory if it doesn't exist.
mkdir -p $TMP

# Change to the temporary directory.
pushd $TMP

# Move the tarball into the temporary directory.
mv /tmp/${USER}_sqli.tar.gz $TMP

# Extract the tarball while preserving permissions and ownerships.
sudo tar -xvpzf ${USER}_sqli.tar.gz

# The FCCU.php file should exist, but still check if it does, then move it.
if [ -f "${TMP}/usr/lib/cgi-bin/FCCU.php" ]; then
    sudo mv "${TMP}/usr/lib/cgi-bin/FCCU.php" "/usr/lib/cgi-bin/"
fi

# The php_practice.php file should exist, but still check if it does, then move it.
if [ -f "${TMP}/var/www/html/php_practice.php" ]; then
    sudo cp "${TMP}/var/www/html/php_practice.php" "/var/www/html/"
fi

# The responses directory should exist, but still check if it does, then move it.
if [ -d "${TMP}/home/.checker/responses" ]; then
    sudo mv "${TMP}/home/.checker/responses" "/home/.checker/"
fi

# Now, restoring the databases.
if [ -f "${TMP}/tmp/save/db_backup.sql" ]; then
    sudo mysql < "${TMP}/tmp/save/db_backup.sql"
fi

# Return to the previous directory.
popd

# Clean up.
# sudo rm -rf $TMP