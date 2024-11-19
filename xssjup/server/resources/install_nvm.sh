#!/bin/bash

# Define the NVM directory.
export HOME="/home/$USER"
export NVM_DIR="$HOME/.nvm"

# Install NVM if not already installed.
if [ ! -d "$NVM_DIR" ]; then
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
fi

# Source NVM.
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# Add NVM source lines to .bashrc if not already present.
if ! grep -q 'export NVM_DIR="$HOME/.nvm"' ~/.bashrc; then
  echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bashrc
  echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.bashrc
  echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"' >> ~/.bashrc
fi

# Install Node.js 18 and set it as default.
nvm install 18
nvm alias default 18
nvm use default

# Navigate to the hidden directory.
cd /home/.checker || { echo "Directory /home/.checker does not exist."; exit 1; }

# Create a minimal package.json if it doesn't exist.
if [ ! -f package.json ]; then
  cat <<EOL > package.json
{
  "name": "checker",
  "version": "1.0.0",
  "description": "A project to install Puppeteer",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "author": "",
  "license": "ISC",
  "dependencies": {}
}
EOL
  echo "Created package.json"
fi

# Install Puppeteer and save it as a dependency.
npm install puppeteer --save
