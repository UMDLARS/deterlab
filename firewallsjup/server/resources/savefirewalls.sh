#!/bin/bash

# Define the temporary directory and current user variables.
export TMP="/tmp/save"
export USER=$(whoami)

# Create the temporary directory if it doesn't exist.
mkdir -p $TMP

# Change to the temporary directory.
pushd $TMP

# Back up the server's firewall rules.
sudo iptables-save > server-rules.v4

# SSH into the client and save the rules directly to the server's /tmp/save directory.
ssh client "sudo iptables-save > /tmp/client-rules.v4"

# SCP the client rules from the client machine to the server's /tmp/save directory.
scp client:/tmp/client-rules.v4 .

# SSH back into the client to delete the rules file.
ssh client "rm -f /tmp/client-rules.v4"

# Create the tarball while preserving permissions and ownerships.
tar --same-owner -cvpzf ${USER}_firewalls.tar.gz \
    --exclude="${USER}_firewalls.tar.gz" \
    /home/.checker/responses \
    server-rules.v4 \
    client-rules.v4

# Move the tarball to the home directory.
sudo chown ${USER}:${USER} ${USER}_firewalls.tar.gz
mv ${USER}_firewalls.tar.gz /home/$USER

# Return to the previous directory.
popd

# Clean up.
sudo rm -rf $TMP
