# -*- coding: utf-8 -*-
"""
Created on Fri May  7 11:40:25 2021

@author: alber

Script to find DNG or NEF not associated with JPG 
"""
import os
import datetime
import time


## CHANGE BEFORE RUN
folder = "/volume1/Personal Alberto/Development" ##Folder to scan
extensions = [".DNG", ".NEF"] ##Extensions to find associated JPG
delete = False ##Delete or not file. If False, it will only print and ouput. Any file will be removed


##initial variables
not_associated = []
size_files = 0
ts = time.time()

##Function to show filesize in human form.
suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

##Check if directory exists
if not os.path.exists(folder):
    print("/!\ Directory doesnt exists: ", folder, "\n")
else:
    print("DIRECTORY TO SCAN: ", folder)


##Double check with the user when delete is activated
if delete:
    temp = input("DELETED MODE ACTIVATED. Are you sure you want to continue?")
    temp = input("PRESS AGAIN TO CONFIRM")
    temp = input("PRESS AGAIN TO CONFIRM - LAST TIME")

    
for root, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            for extension in extensions:
                if filename.endswith(extension):
                    pathtofile = os.path.join(root, filename)
                    ## Check if there is jpg associated to DNG
                    if not os.path.exists(pathtofile.replace(extension, ".JPG")):
                        print(pathtofile)
                        not_associated.append(pathtofile)
                        size_files = size_files + os.path.getsize(pathtofile)
                        if delete:
                            os.remove(os.path.join(root, filename))
                        
##Save loglists with files deleted
with open('not_associated_' + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S') + '.txt', 'w') as f:
    for item in not_associated:
        f.write("%s\n" % item)
        
##Summary output
print(len(not_associated), "files deleted. Cleaned: ", humansize(size_files))
