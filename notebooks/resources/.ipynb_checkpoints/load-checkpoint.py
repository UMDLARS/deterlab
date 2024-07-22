#!/usr/bin/python3
import subprocess
import sys
import os
import time

def main():
    labname = sys.argv[1]

    # Check to see if the node is reachable.
    process = subprocess.run('ping -c 3 ' + labname, shell=True, stdout=subprocess.DEVNULL)

    # Cannot be reached.
    if (process.returncode == 2):
        sys.exit(2)

    # Successfully pinged. Moving data.
    elif (process.returncode == 0):
        # Node is available. Proceed to transfer over the backup.
        process = subprocess.run("scp -i /home/umdsectc/.ssh/merge_key /home/umdsectc/notebooks/saves/umdsectc_" + labname + ".tar.gz umdsectc@" + labname + ":/tmp", shell=True, stdout=subprocess.DEVNULL)

        # Check to make sure that the tarball was transferred before calling the load script for the lab.
        # This is to prevent a race condition, much like the save.py file.
        transfer_success = False

        # Start to validate that the tarball was transferred.
        while (transfer_success == False):
            process = subprocess.run("ssh -i /home/umdsectc/.ssh/merge_key " + labname + " 'test -f /tmp/umdsectc_" + labname + ".tar.gz'", shell=True, stdout=subprocess.DEVNULL)
            if (process.returncode == 0):
                transfer_success = True

        # Transfer validated. Begin the load command for the respective lab.
        process = subprocess.run("ssh -i /home/umdsectc/.ssh/merge_key " + labname + " '/home/.checker/load" + labname + ".sh'", shell=True, stdout=subprocess.DEVNULL)
        print(process)
        sys.exit(0)

    # For other return codes.
    else:
        sys.exit(1)

main()
