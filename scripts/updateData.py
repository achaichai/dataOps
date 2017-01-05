#!/usr/bin/python

"""

Script to update a master dataset

The usage is:
    updateData.py -i <inputFolder> -f <folders>
where
    inputFolder: location of existing master dataset,
    folders:     list of folder names and sizes in MB to increase by in form <name1>,<size1>,...

"""

import argparse
import os
import dataOps

__author__ = 'James Chryssanthacopoulos'

# Constant
bytesInMegabytes = 1048576

# Returns file size of first file in directory
def returnFileSize(folder):
    dirListing = os.listdir(folder)
    
    if not len(dirListing):
        raise Exception('Cannot return file size from empty directory %s' % folder)
    else:
        firstFile = os.path.join(folder, dirListing[0])
        return os.path.getsize(firstFile)


# Define inputs
parser = argparse.ArgumentParser(description = 'Script to update existing master dataset')
parser.add_argument('-i', '--inputFolder', help = 'Location of existing master dataset', required = True)
parser.add_argument('-f', '--folders', help = 'List of folder names and sizes in MB to increase by in form <name1>,<size1>,...', required = True)

# Parse inputs
args = parser.parse_args()
inputFolder = args.inputFolder
folders = args.folders

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
subFolderSizes = [bytesInMegabytes * size for size in subFolderSizes]

# Make input folder if it doesn't already exist
if not os.path.exists(inputFolder):
    raise Exception('Master dataset must exist before running update')

# Create subfolders and files
for subFolder, subFolderSize in zip(subFolders, subFolderSizes):
    # Retrieve file size
    subFolderFullPath = os.path.join(inputFolder, subFolder)
    fileSize = returnFileSize(subFolderFullPath)
    
    # Instantiate a DataUpdater object for the subfolder
    fuObj = dataOps.DataUpdater(subFolderFullPath, fileSize, subFolderSize)

    # Iteratively update files in the subfolder
    fuObj.updateData()