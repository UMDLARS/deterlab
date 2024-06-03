#!/usr/bin/python3

import subprocess
import sys
import os

def main():
    path = os.path.expanduser("~/jupyterintro/")

    # Check to make sure that the path was made.
    ret = os.path.exists(path)

    # Check logs to see if the student made it. Mainly used for save/restore.
    check_job = subprocess.run("screen -ls | grep 'inotify_session' &> /dev/null", shell=True, stdout=subprocess.DEVNULL)

    # If not tracking mkdir, run it. Student may fail the test, but will work if they try again.
    if (check_job.returncode == 1):
        # Missed. Run the job again because it may have been cancelled somehow.
        command = "./run_inotify.sh"
        process = subprocess.run(command, shell=True)

    # mkdir was tracked. Search for it in the logs.
    else:
        if (os.path.exists('/home/.checker/inotify_log.txt')):
            with open('/home/.checker/inotify_log.txt', 'r') as file:
                if "DELETE,ISDIR jupyterintro" in file.read():
                    sys.exit(0)
                else:
                    sys.exit(1)

        # If not entered, it was not picked up from the inotifywait. Simply check if it exists with ret.

    # If not using a restore, just simply check if it exists.
    if ret:
        sys.exit(1)
    else:
        sys.exit(0)

main()
