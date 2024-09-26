#!/usr/bin/python3
import subprocess
import sys
import os
import time

def main():
    labname = sys.argv[1]

    # Remove the existing save so that the new one can be made.
    process = subprocess.run('rm -f /project/USERNAME_GOES_HERE/notebooks/saves/USERNAME_GOES_HERE_' + labname + '.tar.gz', shell=True, stdout=subprocess.DEVNULL)
    print("File removed from ~/notebooks/saves.")

    # Generate the backup. XSS has two nodes, so needs a slightly different statement.
    if (labname == "xss"):
        process = subprocess.run("ssh -i /home/USERNAME_GOES_HERE/.ssh/merge_key USERNAME_GOES_HERE@server '/home/.checker/save" + labname + ".sh'", shell=True, stdout=subprocess.DEVNULL)

    # The firewalls lab needs a special SSH statement, since it relies on environment variables.
    elif (labname == "firewalls"):
        process = subprocess.run('ssh -i /home/USERNAME_GOES_HERE/.ssh/merge_key USERNAME_GOES_HERE@server "bash -l -c \'/home/.checker/savefirewalls.sh\'"', shell=True, stdout=subprocess.DEVNULL)

    # Everything else can be saved the same way.
    else:
        process = subprocess.run("ssh -i /home/USERNAME_GOES_HERE/.ssh/merge_key USERNAME_GOES_HERE@" + labname + " '/home/.checker/save" + labname + ".sh'", shell=True, stdout=subprocess.DEVNULL)
        
    print("Backup tarball created.")


    
    # Get the backup into the XDC, then transfer it.
    if (labname == "xss" or labname == "firewalls"):
        process = subprocess.run("scp -i /home/USERNAME_GOES_HERE/.ssh/merge_key USERNAME_GOES_HERE@server:~/USERNAME_GOES_HERE_" + labname + ".tar.gz /project/USERNAME_GOES_HERE/notebooks/saves &> /dev/null", shell=True, stdout=subprocess.DEVNULL)

    else:
        process = subprocess.run("scp -i /home/USERNAME_GOES_HERE/.ssh/merge_key USERNAME_GOES_HERE@" + labname + ":~/USERNAME_GOES_HERE_" + labname + ".tar.gz /project/USERNAME_GOES_HERE/notebooks/saves &> /dev/null", shell=True, stdout=subprocess.DEVNULL)
        
    print("Copied onto the XDC.")


    
    # Wait until the file is FULLY transferred before deleting remotely.
    # This is a race condition that happens due to bandwidth.
    while not os.path.exists("/project/USERNAME_GOES_HERE/notebooks/saves/USERNAME_GOES_HERE_" + labname + ".tar.gz"):
        time.sleep(1)


    
    # Delete the lab's tarball remotely.
    if (labname == "xss" or labname == "firewalls"):
        process = subprocess.run("ssh -i /home/USERNAME_GOES_HERE/.ssh/merge_key USERNAME_GOES_HERE@server 'rm -f USERNAME_GOES_HERE_" + labname + ".tar.gz &> /dev/null'", shell=True, stdout=subprocess.DEVNULL)

    else:
        process = subprocess.run("ssh -i /home/USERNAME_GOES_HERE/.ssh/merge_key USERNAME_GOES_HERE@" + labname + " 'rm -f USERNAME_GOES_HERE_" + labname + ".tar.gz &> /dev/null'", shell=True, stdout=subprocess.DEVNULL)

    print("File removed remotely.")

main()
