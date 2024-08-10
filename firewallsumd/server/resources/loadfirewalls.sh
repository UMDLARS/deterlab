# Define the temporary directory and current user variables.
export TMP="/tmp/load"
export USER=$(whoami)

# Create the temporary directory if it doesn't exist.
mkdir -p $TMP

# Change to the temporary directory.
pushd $TMP

# Move the tarball into the temporary directory.
mv /tmp/${USER}_firewalls.tar.gz $TMP

# Extract the tarball while preserving permissions and ownerships.
tar -xvpzf ${USER}_firewalls.tar.gz

# Check and move the responses directory, overwriting if it exists.
if [ -d "${TMP}/home/.checker/responses" ]; then
    sudo rm -rf "/home/.checker/responses"
    sudo mv "${TMP}/home/.checker/responses" "/home/.checker/"
fi

# Restoring the iptables rules.
sudo iptables-restore < server-rules.v4

# Transfer the client-rules.v4 file back to the client node.
scp client-rules.v4 client:/tmp/client-rules.v4

# SSH into the client and restore the iptables rules.
ssh client "sudo iptables-restore < /tmp/client-rules.v4 && rm -f /tmp/client-rules.v4"

# Return to the previous directory.
popd

sudo rm -rf $TMP
