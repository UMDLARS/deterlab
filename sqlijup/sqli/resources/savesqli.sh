#!/bin/bash

# Define the temporary directory and current user variables.
export TMP="/tmp/save"
export USER=$(whoami)

# Create the temporary directory if it doesn't exist.
mkdir -p $TMP

# Change to the temporary directory.
pushd $TMP

# Before creating the tarball, we need a backup of the databases.
sudo mysqldump --databases fccu practice > ${TMP}/db_backup.sql

# Create the tarball while preserving permissions and ownerships.
sudo tar --same-owner -cvpzf ${USER}_sqli.tar.gz \
    --exclude="${USER}_sqli.tar.gz" \
    /usr/lib/cgi-bin/FCCU.php \
    /var/www/html/php_practice.php \
    /home/.checker/responses \
    ${TMP}/db_backup.sql

# Move the tarball to the home directory.
sudo chown ${USER}:${USER} ${USER}_sqli.tar.gz
mv ${USER}_sqli.tar.gz /home/$USER

# Return to the previous directory.
popd

# Clean up.
sudo rm -rf $TMP