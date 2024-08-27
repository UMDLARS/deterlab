#!/bin/bash

# Create a new, detached screen session with the inotifywait session to recursively track the home directory.

screen -dmS inotify_session bash -c "inotifywait -m -r -e create -e delete -e attrib ~ > /home/.checker/inotify_log.txt"