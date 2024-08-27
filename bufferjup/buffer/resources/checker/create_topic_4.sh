# First, make sure that the folder isn't already made.
if [ -d "~/topic_4/" ]; then
    exit
fi

# Otherwise, start setting it up.
mkdir ~/topic_4/
cd ~/topic_4/
git clone https://github.com/UMDLARS/wormwood
mv wormwood/ wormwood_fix/
git clone https://github.com/UMDLARS/wormwood
mv wormwood/ wormwood_test/

# Revoke writing access for the test directory. Students should not touch this.
chmod -R a-w wormwood_test/
