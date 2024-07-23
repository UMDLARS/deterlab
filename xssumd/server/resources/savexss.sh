#!/bin/bash

# Define the temporary directory and current user variables.
export TMP="/tmp/save"
export USER=$(whoami)

# Create the temporary directory if it doesn't exist.
mkdir -p $TMP

# Change to the temporary directory.
pushd $TMP

# Before creating the tarball, we need a backup of the databases.
sudo mysqldump --databases forum xss > ${TMP}/db_backup.sql

# Create the tarball while preserving permissions and ownerships.
sudo tar --same-owner -cvpzf ${USER}_xss.tar.gz \
    --exclude="${USER}_xss.tar.gz" \
    /var/www/html/sanitize.php \
    /home/.checker/responses \
    /home/.checker/section_2.js \
    /home/.checker/section_2.py \
    ${TMP}/db_backup.sql

# Move the tarball to the home directory.
sudo chown ${USER}:${USER} ${USER}_xss.tar.gz
mv ${USER}_xss.tar.gz /home/$USER

# Return to the previous directory.
popd

# Clean up.
sudo rm -rf $TMP