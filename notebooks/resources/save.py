#!/usr/bin/python3
import subprocess
import sys
import os
import time

def main():
    labname = sys.argv[1]

    # Remove the existing save so that the new one can be made.
    process = subprocess.run('rm -f /home/umdsectc/notebooks/saves/umdsectc_' + labname + '.tar.gz', shell=True, stdout=subprocess.DEVNULL)
    print("File removed from ~/notebooks/saves.")

    # Generate the backup.
    process = subprocess.run("ssh -i /home/umdsectc/.ssh/merge_key umdsectc@" + labname + " '/home/.checker/save" + labname + ".sh'", shell=True, stdout=subprocess.DEVNULL)
    print("Backup tarball created.")

    # Get the backup into the XDC, then transfer it.
    process = subprocess.run("scp -i /home/umdsectc/.ssh/merge_key umdsectc@" + labname + ":~/umdsectc_" + labname + ".tar.gz /home/umdsectc/notebooks/saves &> /dev/null", shell=True, stdout=subprocess.DEVNULL)
    print("Copied onto the XDC.")

    # Wait until the file is FULLY transferred before deleting remotely.
    # This is a race condition that happens due to bandwidth.
    while not os.path.exists("/home/umdsectc/notebooks/saves/umdsectc_" + labname + ".tar.gz"):
        time.sleep(1)

    # Delete the lab's tarball remotely.
    process = subprocess.run("ssh -i /home/umdsectc/.ssh/merge_key umdsectc@" + labname + " 'rm -f umdsectc_" + labname + ".tar.gz &> /dev/null'", shell=True, stdout=subprocess.DEVNULL)
    print("File removed remotely.")

main()
