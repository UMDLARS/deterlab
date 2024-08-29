# Define the temporary directory and current user variables.
export TMP="/tmp/load"
export USER=$(whoami)

# Create the temporary directory if it doesn't exist.
mkdir -p $TMP

# Change to the temporary directory.
pushd $TMP

# Move the tarball into the temporary directory.
mv /tmp/${USER}_intro.tar.gz $TMP

# Extract the tarball.
tar -xvf ${TMP}/${USER}_intro.tar.gz

# Check if findme.txt exists in the temporary directory and copy it if it does.
if [ -e "${TMP}/findme.txt" ]; then
    cp "${TMP}/findme.txt" "/usr/share/discover/dtd/findme.txt"
fi

# Check if the home directory exists (which it should), then copy it if it does.
if [ -e "${TMP}/${USER}" ]; then
    cp -r ${TMP}/${USER}/* ~
fi

# Check if .inotify_log.txt exists in the temporary directory and copy it if it does.
if [ -e "${TMP}/inotify_log.txt" ]; then
    cp "${TMP}/inotify_log.txt" "/home/.checker/inotify_log.txt"
fi

# Return to the previous directory.
popd

# Clean up.
#rm -f /tmp/${USER}_intro.tar.gz
#rm -r $TMP
