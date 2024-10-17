#!/bin/bash

export USER="$(whoami)"
export LABS="/project/$USER/notebooks"
export RESOURCES="$LABS/resources"
export SAVES="$LABS/saves"
export EDUCATION="/home/.education"

# Check if the student is running as root.
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run this script as sudo."
    exit 1
fi

# Define the directory where the repository should be checked out.
REPO_URL="https://github.com/UMDLARS/deterlab"

# Installing some dependencies.
echo "Installing dependencies."
sudo apt-get -qq update
sudo apt-get -qq install git rsync >/dev/null

# sudo is required for these, since the notebooks are ran as root. Hiding the warning about installing packages as root.
echo "Installing required Jupyter extensions."
sudo pip install -q ipywidgets jupyterlab_widgets 2>/dev/null

echo "Beginning installation of notebooks."

# Use a temporary directory for cloning.
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR" || exit

# Clone the repository.
git clone "$REPO_URL"
if [ $? -ne 0 ]; then
    echo -e "\033[0;31mFailed to clone the repository. Exiting.\033[0m"
    exit 1
fi

cd deterlab || exit

# Checking to see if the notebooks have already been made.
if [ $(find "$LABS" -maxdepth 1 -type f -name "*.ipynb" | wc -l) -eq 8 ]; then
    echo -e "\033[0;31mYour notebooks already exist. Updating your notebooks...\033[0m"
else
    echo -e "\033[0;31mSome (or all) of your notebooks appear to be missing. Adding them...\033[0m"
fi

# Excluding the saves/ directory so that students don't lose their saves.
sudo rsync -a --delete --exclude='saves/' notebooks/ /project/$USER/notebooks/ >/dev/null

# Ensure 'saves/' exists.
mkdir -p "$LABS/saves"

# Move the lab resources.
LOG_FILE="${EDUCATION}/${USER}_logs.txt"
TEMP_LOG="/tmp/${USER}_logs.txt"

if [ -d "$EDUCATION" ]; then
    echo -e "\033[0;31mLab resources for your notebooks already exist. Applying updates...\033[0m"

    # Preserve the log file by copying it to a temporary location
    if [ -f "$LOG_FILE" ]; then
        sudo cp "$LOG_FILE" "$TEMP_LOG"
    fi

    # Delete everything except the log file.
    sudo find "$EDUCATION" -mindepth 1 ! -name "$(basename "$LOG_FILE")" -exec rm -rf {} +

else
    echo -e "\033[0;31mLab resources do not exist on your XDC. Creating them...\033[0m"
    sudo mkdir -p "$EDUCATION"
    sudo chown -R "$USER:$USER" "$EDUCATION"
fi

# Restore the log file if it was preserved.
if [ -f "$TEMP_LOG" ]; then
    sudo mv "$TEMP_LOG" "$EDUCATION/"
    sudo chown $USER:$USER "$EDUCATION/$(basename "$TEMP_LOG")"
fi

# Find and copy all directories ending with 'jup' to the $EDUCATION directory
for dir in $(find . -maxdepth 1 -type d -name "*jup"); do
    dir_name=$(basename "$dir")
    sudo mv "$dir_name" "$EDUCATION"
done

# Move the grades back for the student.
[ -f "/tmp/${USER}_logs.txt" ] && sudo mv "/tmp/${USER}_logs.txt" "$EDUCATION"

# Finally, copy all of the notebook function files (should be four of them) into the student's XDC.
sudo mv runlab startexp stopexp runr /home
sudo mv grader.py "$EDUCATION"
sudo chmod a+x /home/runlab /home/startexp /home/stopexp /home/runr "$EDUCATION/grader.py"

# Cleanup temporary directory.
rm -rf "$TEMP_DIR"

# Configure all labs to work with the current username.
pushd "$LABS" > /dev/null 2>&1
for notebook in *.ipynb; do
    sed -i "s/USERNAME_GOES_HERE/$USER/g" "$notebook"
done

# Change the USERNAME_GOES_HERE occurrence in the port forwarding script.
sed -i "s/USERNAME_GOES_HERE/$USER/g" "$LABS/resources/port-forward/port-forward-setup"

# Doing the same for the save/load scripts.
sed -i "s/USERNAME_GOES_HERE/$USER/g" "$LABS/resources/save.py"
sed -i "s/USERNAME_GOES_HERE/$USER/g" "$LABS/resources/load.py"
popd > /dev/null 2>&1

# And finally, for the install scripts.
sudo find "$EDUCATION" -type f -name install -exec sed -i "s/USERNAME_GOES_HERE/$USER/g" {} +

echo -e "\033[0;32mDone. You can find your notebooks in $LABS. Please refresh your browser's tab before starting a lab.\033[0m"
