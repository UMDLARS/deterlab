#!/bin/bash

export USER="$(whoami)"
export LABS="$HOME/notebooks"
export RESOURCES="$LABS/resources"
export SAVES="$LABS/saves"
export EDUCATION="$HOME/.education"

echo "Installing dependencies."
sudo apt-get -qq update
sudo apt-get -qq install git

echo "Installing required Jupyter extensions."
sudo pip install -q ipywidgets jupyterlab_widgets 2>/dev/null

echo "Beginning installation of notebooks."
mkdir -p "$LABS" > /dev/null 2>&1

# Use a temporary directory for cloning.
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR" || exit

# Checking to see if the notebooks have already been made.
if [ $(find "$LABS" -maxdepth 1 -type f -name "*.ipynb" | wc -l) -eq 8 ]; then
    echo -e "\033[0;31mA notebook directory already exists. Updating your notebooks...\033[0m"
    if [ -d "$LABS/.git" ]; then
        cd "$LABS" || exit
        git pull --quiet
    fi
else
    # Clone the repository.
    git clone --no-checkout https://github.com/UMDLARS/deterlab --quiet
    if [ $? -ne 0 ]; then
        echo -e "\033[0;31mFailed to clone the repository. Exiting.\033[0m"
        exit 1
    fi

    cd deterlab || exit
    git sparse-checkout init --cone
    git sparse-checkout set notebooks
    git checkout main --quiet
    if [ $? -ne 0 ]; then
        echo -e "\033[0;31mFailed to checkout the main branch. Exiting.\033[0m"
        exit 1
    fi
    
    # Move the notebooks directory to the desired location.
    mv notebooks/* "$LABS/"
    
    # Initialize $LABS as a Git repository for future updates.
    cd "$LABS" || exit
    git init --quiet
    git remote add origin https://github.com/UMDLARS/deterlab
    git sparse-checkout init --cone
    git sparse-checkout set notebooks
fi

# Cleanup temporary directory.
cd "$HOME"
rm -rf "$TEMP_DIR"

mkdir -p "$SAVES" > /dev/null 2>&1
if [ $? -eq 1 ]; then
    echo -e "\033[0;31mA saves folder already exists.\033[0m"
fi

# Define the directory where the repository should be checked out.
REPO_URL="https://github.com/UMDLARS/deterlab"

# Check if /home/.education exists.
if [ -d "/home/.education" ]; then
    echo -e "\033[0;32m/home/.education exists. Pulling updates...\033[0m"
    if [ -d "/home/.education/.git" ]; then
        cd "/home/.education" || exit
        git pull --quiet
    fi
else
    sudo mkdir -p "/home/.education"
    sudo chown -R "$USER:$USER" "/home/.education"
    
    # Clone the repository.
    git clone --no-checkout "$REPO_URL" "/home/.education" --quiet
    if [ $? -ne 0 ]; then
        echo -e "\033[0;31mFailed to clone the repository. Exiting.\033[0m"
        exit 1
    fi

    cd "/home/.education" || exit
    
    # Initialize sparse-checkout.
    git sparse-checkout init
    echo "/*" > .git/info/sparse-checkout
    echo "!/notebooks/" >> .git/info/sparse-checkout
    echo "!/install_notebooks.sh" >> .git/info/sparse-checkout
    
    # Checkout the repository.
    git checkout main --quiet
    if [ $? -ne 0 ]; then
        echo -e "\033[0;31mFailed to checkout the main branch. Exiting.\033[0m"
        exit 1
    fi
fi

# Configure all labs to work with the current username.
pushd "$LABS" > /dev/null 2>&1
for notebook in *.ipynb; do
    sed -i "s/USERNAME_GOES_HERE/$USER/g" "$notebook"
done
popd > /dev/null 2>&1

echo -e "\033[0;32mDone. You can find your notebooks in $LABS. Please refresh your browser's tab before starting a lab.\033[0m"
