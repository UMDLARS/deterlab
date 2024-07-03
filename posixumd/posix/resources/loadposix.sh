#!/bin/bash

# Define the temporary directory and current user variables.
export TMP="/tmp/load"
export USER=$(whoami)

# Create the temporary directory if it doesn't exist.
mkdir -p $TMP

# Change to the temporary directory.
pushd $TMP

# Move the tarball into the temporary directory.
mv /tmp/${USER}_posix.tar.gz $TMP

# Extract the tarball while preserving permissions and ownerships.
sudo tar -xvpzf ${USER}_posix.tar.gz

# Check if the home directory contents exist in the temporary directory and move them to the appropriate places.
# Need to use the find command for this, since cp and mv are not working with directories and keeping permissions.
# The find command will limit the search to the immediate contents of the directory, then executes the move command of find's match
# to move the contents into the home directory.
if [ -d "${TMP}/home/${USER}/posix_practice/" ]; then
    sudo find "${TMP}/home/${USER}/posix_practice/" -mindepth 1 -maxdepth 1 -exec mv -t "/home/${USER}/posix_practice/" {} +
fi

if [ -d "${TMP}/home/${USER}/special_permissions/" ]; then
    sudo find "${TMP}/home/${USER}/special_permissions/" -mindepth 1 -maxdepth 1 -exec mv -t "/home/${USER}/special_permissions/" {} +
fi

# Check if /collections/ exists, move it if it does.
if [ -d "${TMP}/collections/" ]; then
    sudo mv "${TMP}/collections/" "/"
fi

# Checking if other users have been made and move them if they exist.
if [ -d "${TMP}/home/ash" ]; then
    sudo mv "${TMP}/home/ash/" "/home/"
fi

if [ -d "${TMP}/home/brock" ]; then
    sudo mv "${TMP}/home/brock/" "/home/"
fi

if [ -d "${TMP}/home/misty" ]; then
    sudo mv "${TMP}/home/misty/" "/home/"
fi

if [ -d "${TMP}/home/james" ]; then
    sudo mv "${TMP}/home/james/" "/home/"
fi

# Check if the student has responses, and move them if they do.
if [ -d "${TMP}/home/.checker/responses" ]; then
    sudo mv "${TMP}/home/.checker/responses/" "/home/.checker/"
fi

# Copy the users/groups back.
if [ -f "${TMP}/etc/passwd" ]; then
    sudo mv "${TMP}/etc/passwd" "/etc/"
fi

if [ -f "${TMP}/etc/group" ]; then
    sudo mv "${TMP}/etc/group" "/etc/"
fi

if [ -f "${TMP}/etc/shadow" ]; then
    sudo mv "${TMP}/etc/shadow" "/etc/"
fi

# Return to the previous directory.
popd

# Clean up.
# rm -f $TMP/${USER}_posix.tar.gz
# sudo rm -rf $TMP
