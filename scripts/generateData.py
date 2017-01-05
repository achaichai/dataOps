#!/usr/bin/python

"""

Script to generate the master dataset

The usage is:
    generateData.py -i <inputFolder> -s <fileSize> -f <folders>
where:
    inputFolder: location where master dataset should be written,
    fileSize:    file size in MB,
    folders:     list of folder names and sizes in MB in form <name1>,<size1>,...

"""

import argparse
import os
import dataOps

__author__ = 'James Chryssanthacopoulos'

# Constant
bytesInMegabytes = 1048576

# Define inputs
parser = argparse.ArgumentParser(description = 'Script to generate the master dataset')
parser.add_argument('-i', '--inputFolder', help = 'Location where master dataset should be written', required = True)
parser.add_argument('-s', '--fileSize', help = 'File size in MB', required = True)
parser.add_argument('-f', '--folders', help = 'List of folder names and sizes in MB in form <name1>,<size1>,...', required = True)

# Parse inputs
args = parser.parse_args()
inputFolder = args.inputFolder
fileSize = args.fileSize
folders = args.folders

# Convert file size to an integer
if not fileSize.isdigit():
    raise Exception('-s must be an integer')
else:
    fileSize = int(fileSize)

# Find subfolder names and sizes
foldersAndSizes = folders.split(',')
if len(foldersAndSizes) % 2 != 0:
    raise Exception('-f option must have an even number of elements')

# Find number of subfolders
numSubFolders = len(foldersAndSizes) / 2

# Parse subfolder names and sizes
subFolders = [0] * numSubFolders
subFolderSizes = [0] * numSubFolders
idx = 0
for i in range(numSubFolders):
    subFolders[i] = foldersAndSizes[idx]
    
    if not foldersAndSizes[idx + 1].isdigit():
        raise Exception('Folder sizes in -f option must be positive integers')
    else:
        subFolderSizes[i] = int(foldersAndSizes[idx + 1])
    
    idx += 2
    
# Convert file sizes to bytes
fileSize *= bytesInMegabytes
subFolderSizes = [bytesInMegabytes * size for size in subFolderSizes]

# Make input folder if it doesn't already exist
if not os.path.exists(inputFolder):
    os.makedirs(inputFolder)

# Create subfolders and files
for subFolder, subFolderSize in zip(subFolders, subFolderSizes):
    # Instantiate a DataInitializer object for the subfolder
    subFolderFullPath = os.path.join(inputFolder, subFolder)
    fiObj = dataOps.DataInitializer(subFolderFullPath, fileSize, subFolderSize)

    # Iteratively write files in the subfolder
    fiObj.writeData()