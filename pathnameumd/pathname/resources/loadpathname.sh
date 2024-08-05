# Define the temporary directory and current user variables.
export TMP="/tmp/load"
export USER=$(whoami)

# Create the temporary directory if it doesn't exist.
mkdir -p $TMP

# Change to the temporary directory.
pushd $TMP

# Move the tarball into the temporary directory.
mv /tmp/${USER}_pathname.tar.gz $TMP

# Extract the tarball while preserving permissions and ownerships.
tar -xvpzf ${USER}_pathname.tar.gz

# Check and move the responses directory, overwriting if it exists.
if [ -d "${TMP}/home/.checker/responses" ]; then
    sudo rm -rf "/home/.checker/responses"
    sudo mv "${TMP}/home/.checker/responses" "/home/.checker/"
fi

# Copy all files over to the home directory.
if [ -d "${TMP}/home/${USER}" ]; then
    sudo mv ${TMP}/home/${USER}/* /home/${USER}/
fi

# Copy all files into the /lab directory.
if [ -d "${TMP}/lab" ]; then
    sudo mv ${TMP}/lab /
fi

# Return to the previous directory.
popd

# Clean up.
sudo rm -rf $TMP