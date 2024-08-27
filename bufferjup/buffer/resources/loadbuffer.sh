# Define the temporary directory and current user variables.
export TMP="/tmp/load"
export USER=$(whoami)

# Create the temporary directory if it doesn't exist.
mkdir -p $TMP

# Change to the temporary directory.
pushd $TMP

# Move the tarball into the temporary directory.
mv /tmp/${USER}_buffer.tar.gz $TMP

# Extract the tarball while preserving permissions and ownerships.
tar -xvpzf ${USER}_buffer.tar.gz

# Check and move the responses directory, overwriting if it exists.
if [ -d "${TMP}/home/.checker/responses" ]; then
    sudo rm -rf "/home/.checker/responses"
    sudo mv "${TMP}/home/.checker/responses" "/home/.checker/"
fi

# Copy all files over to the home directory.
if [ -d "${TMP}/home/${USER}" ]; then
    sudo rm -rf "/home/${USER}/topic_*"
    sudo mv ${TMP}/home/${USER}/* /home/${USER}/
fi

# Check to see if the topic_4/ directory exists.
if [ -d "/home/${USER}/topic_4/" ]; then
    # Look in the wormwood_test directory. If it doesn't have a build directory, make it.
    if [ ! -d "/home/${USER}/topic_4/wormwood_test/build" ]; then
        mkdir -p "/home/${USER}/topic_4/wormwood_test/build"
        cd "/home/${USER}/topic_4/wormwood_test/build"
        cmake ..
    fi

    # Look in the wormwood_fix directory. If it doesn't have a build directory, make it.
    if [ ! -d "/home/${USER}/topic_4/wormwood_fix/build" ]; then
        mkdir -p "/home/${USER}/topic_4/wormwood_fix/build"
        cd "/home/${USER}/topic_4/wormwood_fix/build"
        cmake ..
    fi
fi

# Return to the previous directory.
popd

