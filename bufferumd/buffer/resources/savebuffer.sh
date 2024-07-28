#!/bin/bash

# Define the temporary directory and current user variables.
export TMP="/tmp/save"
export USER=$(whoami)

# Create the temporary directory if it doesn't exist.
mkdir -p $TMP

# Change to the temporary directory.
pushd $TMP

# Create the tarball while preserving permissions and ownerships.
tar --same-owner -cvpzf ${USER}_buffer.tar.gz \
    --exclude="${USER}_buffer.tar.gz" \
    --exclude="/home/$USER/.*" \
    --exclude="/home/$USER/../.*" \
    --exclude="/home/$USER/../*/.*" \
    --exclude="/home/$USER/../*/../.*" \
    /home/$USER \
    /home/.checker/responses

# Move the tarball to the home directory.
sudo chown ${USER}:${USER} ${USER}_buffer.tar.gz
mv ${USER}_buffer.tar.gz /home/$USER

# Return to the previous directory.
popd

# Clean up.
sudo rm -rf $TMP
