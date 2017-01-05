#!/usr/bin/python

"""

Script to backup a master dataset

The usage is:
    backupData.py -i <inputFolder> -b <backupFolder>
where:
    inputFolder:  location of existing master dataset,
    backupFolder: location of backup folder

"""

import argparse
import dataOps

__author__ = 'James Chryssanthacopoulos'


# Define inputs
parser = argparse.ArgumentParser(description = 'Script to backup a master dataset')
parser.add_argument('-i', '--inputFolder', help = 'Location of existing master dataset', required = True)
parser.add_argument('-b', '--backupFolder', help = 'Location of backup folder', required = True)

# Parse inputs
args = parser.parse_args()
inputFolder = args.inputFolder
backupFolder = args.backupFolder

# Backup input folder
dataOps.DataBackup().backup(inputFolder, backupFolder)