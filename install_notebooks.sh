#!/bin/bash

export USER="$(whoami)"
export LABS="$HOME/notebooks"
export RESOURCES="$LABS/resources"
export SAVES="$LABS/saves"
export EDUCATION="$HOME/.education"

# Define the directory where the repository should be checked out.
REPO_URL="https://github.com/UMDLARS/deterlab"

echo "Installing dependencies."
sudo apt-get -qq update
sudo apt-get -qq install git rsync >/dev/null

# sudo is required for these, since the notebooks are ran as root. Hiding the warning about installing packages as root.
echo "Installing required Jupyter extensions."
sudo pip install -q ipywidgets jupyterlab_widgets 2>/dev/null

echo "Beginning installation of notebooks."
mkdir -p "$LABS" > /dev/null 2>&1

# Use a temporary directory for cloning.
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR" || exit

# Clone the repository.
git clone --no-checkout "$REPO_URL" --quiet
if [ $? -ne 0 ]; then
    echo -e "\033[0;31mFailed to clone the repository. Exiting.\033[0m"
    exit 1
fi

cd deterlab || exit
git checkout main --quiet
if [ $? -ne 0 ]; then
    echo -e "\033[0;31mFailed to checkout the main branch. Exiting.\033[0m"
    exit 1
fi

# If it exists, copy the saves/ directory into /tmp so that students don't lose progress.
cp -r ~/notebooks/saves /tmp 2>/dev/null

# Checking to see if the notebooks have already been made.
if [ $(find "$LABS" -maxdepth 1 -type f -name "*.ipynb" | wc -l) -eq 8 ]; then
    echo -e "\033[0;31mYour notebooks already exist. Updating your notebooks...\033[0m"
else
    echo -e "\033[0;31mSome (or all) of your notebooks appear to be missing. Adding them...\033[0m"
fi

# Move the notebooks directory to the home directory. Using rsync because moving from the /tmp directory fixes any cross-filesystem move errors.
# -a preserves permissions, timestamps, etc.
rm -rf ~/notebooks
rsync -a --remove-source-files --delete notebooks/ ~/notebooks >/dev/null

# Move the saves back and delete it from /tmp.
[ -d /tmp/saves ] && mv /tmp/saves $LABS

# If no saves/ directory existed, then create it.
mkdir -p ~/notebooks/saves

# Move the lab resources.
if [ -d "/home/.education" ]; then
    echo -e "\033[0;31mLab resources for your notebooks already exist. Applying updates...\033[0m"
else
    echo -e "\033[0;31mLab resources do not exist on your XDC. Creating them...\033[0m"
    sudo mkdir -p "/home/.education"
    sudo chown -R "$USER:$USER" "/home/.education"
fi

rsync -a --remove-source-files *jup/ "$EDUCATION/"

# Finally, copy all of the notebook function files (should be four of them) into the student's XDC.
sudo mv runlab startexp stopexp runr /home
sudo chmod a+x runlab startexp stopexp runr

# Cleanup temporary directory.
rm -rf "$TEMP_DIR"

# Configure all labs to work with the current username.
pushd "$LABS" > /dev/null 2>&1
for notebook in *.ipynb; do
    sed -i "s/USERNAME_GOES_HERE/$USER/g" "$notebook"
done
popd > /dev/null 2>&1

echo -e "\033[0;32mDone. You can find your notebooks in $LABS. Please refresh your browser's tab before starting a lab.\033[0m"
