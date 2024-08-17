#!/bin/bash

export USER="$(whoami)"
export LABS="/home/$USER/notebooks"
export RESOURCES="$LABS/resources"
export SAVES="$LABS/saves"
export EDUCATION="/home/.education"

echo "Installing dependencies."

sudo apt-get -qq update
sudo apt-get -qq install git

echo "Installing required Jupyter extensions."

# Hide the warning about pip not being used with sudo. Notebooks are ran as root, so this is required.
sudo pip install -q ipywidgets jupyterlab_widgets 2>/dev/null

# Copying over the notebooks.
echo "Beginning installation of notebooks."
mkdir -p $LABS > /dev/null 2>&1

# Use a temporary directory for cloning
TEMP_DIR=$(mktemp -d)
cd $TEMP_DIR

# Checking to see if the notebooks have already been made.
if [ $(find $LABS -maxdepth 1 -type f -name "*.ipynb" | wc -l) -eq 8 ]; then
    echo -e "\033[0;31mNotebooks already exist. Updating your notebooks...\033[0m"
    cd $LABS
    git pull --quiet
else
    # Clone the repository
    git clone --no-checkout https://github.com/UMDLARS/deterlab --quiet
    if [ $? -ne 0 ]; then
        echo -e "\033[0;31mFailed to clone the repository. Exiting.\033[0m"
        exit 1
    fi

    cd deterlab
    git sparse-checkout init --cone
    git sparse-checkout set notebooks
    git checkout main --quiet
    if [ $? -ne 0 ]; then
        echo -e "\033[0;31mFailed to checkout the main branch. Exiting.\033[0m"
        exit 1
    fi
    
    # Move the notebooks directory to the desired location
    mv notebooks/* $LABS/
fi

mkdir -p $SAVES > /dev/null 2>&1
if [ $? -eq 1 ]; then
    echo -e "\033[0;31mA saves folder already exists.\033[0m"
fi

# Clone or update other directories into /home/.education
if [ -d "$EDUCATION" ]; then
    echo -e "\033[0;31mEducation directory already exists. Updating...\033[0m"
    cd $EDUCATION
    git pull --quiet
else
    echo "Cloning other directories into /home/.education"
    mkdir -p $EDUCATION
    cd $EDUCATION
    git clone --no-checkout https://github.com/UMDLARS/deterlab --quiet
    if [ $? -ne 0 ]; then
        echo -e "\033[0;31mFailed to clone the repository. Exiting.\033[0m"
        exit 1
    fi
    
    git sparse-checkout init --cone
    git sparse-checkout set "/*" "!notebooks/"
    git checkout main --quiet
    if [ $? -ne 0 ]; then
        echo -e "\033[0;31mFailed to checkout the main branch. Exiting.\033[0m"
        exit 1
    fi
fi

# Configure all labs to work with the current username.
pushd $LABS > /dev/null 2>&1
for notebook in *.ipynb; do
    sed -i "s/USERNAME_GOES_HERE/$USER/g" "$notebook"
done
popd > /dev/null 2>&1

echo -e "\033[0;32mDone. You can find your notebooks in $LABS and other files in $EDUCATION. Please refresh your browser's tab before starting a lab.\033[0m"
