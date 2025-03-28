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

# Check if inotify_log.txt exists in the temporary directory and copy it if it does.
if [ -e "${TMP}/inotify_log.txt" ]; then
    cp "${TMP}/inotify_log.txt" "/home/.checker/inotify_log.txt"
fi

# Check if inotify_log.txt exists in the temporary directory and copy it if it does.
if [ -e "${TMP}/step2_perms.txt" ]; then
    cp "${TMP}/step2_perms.txt" "/home/.checker/step2_perms.txt"
fi

# Check if findme.txt exists in the temporary directory and copy it if it does.
if [ -e "${TMP}/.findme.txt" ]; then
    cp "${TMP}/.findme.txt" "/usr/share/discover/dtd/.findme.txt"
else
    sudo rm -f "/usr/share/discover/dtd/.findme.txt"
fi

# Check if /step_12_answer.txt exists in the temporary directory and copy it if it does.
if [ -e "${TMP}/step_12_answer.txt" ]; then
    cp "${TMP}/step_12_answer.txt" "/home/.checker/step_12_answer.txt"
fi

# Check if the home directory exists (which it should), then copy it if it does.
if [ -e "${TMP}/${USER}" ]; then
    cp -r ${TMP}/${USER}/* ~
fi

# Return to the previous directory.
popd

# Clean up.
rm -f /tmp/${USER}_intro.tar.gz
rm -r $TMP
