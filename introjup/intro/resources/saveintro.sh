# Define the temporary directory and current user variables.
export TMP="/tmp/save"
export USER=$(whoami)

# Create the temporary directory if it doesn't exist.
mkdir -p $TMP

# Change to the temporary directory.
pushd $TMP

# Check if inotify_log.txt exists in the temporary directory and copy it if it does.
if [ -e "/home/.checker/inotify_log.txt" ]; then
    cp "/home/.checker/inotify_log.txt" $TMP
fi

# Check if step2_perms.txt exists in the temporary directory and copy it if it does.
if [ -e "/home/.checker/step2_perms.txt" ]; then
    cp "/home/.checker/step2_perms.txt" $TMP
fi

# Check if findme.txt exists in the temporary directory and copy it if it does.
if [ -e "/usr/share/discover/dtd/.findme.txt" ]; then
    cp "/usr/share/discover/dtd/.findme.txt" $TMP
fi

# Check if the home directory exists (which it should), then copy it if it does.
if [ -e "/home/${USER}" ]; then
    cp -r "/home/${USER}" $TMP
fi

# Check if the student answered Step 12, then copy it if they did.
if [ -e "/home/.checker/step_12_answer.txt" ]; then
    cp -r "/home/.checker/step_12_answer.txt" $TMP
fi

# Create the tarball, then move it to the home directory temporarily to scp it over.
tar -cvf ${USER}_intro.tar.gz .
mv ${TMP}/${USER}_intro.tar.gz ~

# Return to the previous directory.
popd

# Clean up.
rm -r $TMP
