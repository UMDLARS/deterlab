#!/bin/bash

export USER="$(whoami)"
export LABS="/home/$USER/notebooks"

echo "Installing required Jupyter extensions."

# sudo is required, since the labs are ran as root.
sudo pip install -q ipywidgets jupyterlab_widgets

echo "Beginning installation of notebooks."

mkdir $LABS > /dev/null 2>&1
if [ $? -eq 1 ]; then
    echo -e "\033[0;31mA notebook folder already exists. Copying the notebooks into your folder...\033[0m"
fi
# Replace the next line in the future with /share/education/new_labs or something similar.
cp /home/labs/* $LABS

# Configure all labs to work with the current username.
pushd $LABS > /dev/null 2>&1
for notebook in *.ipynb; do
    sed -i "s/umdsecXX/$USER/g" "$notebook"
done

echo -e "\033[0;32mDone. You can find your notebooks in $LABS. Please refresh your browser's tab before starting a lab.\033[0m"

