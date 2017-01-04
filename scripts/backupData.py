#!/usr/bin/python

"""

Script to backup a master dataset

The usage is:
    backupData.py -i <inputFolder> -b <backupFolder>

"""

import argparse
import dataOps

__author__ = 'James Chryssanthacopoulos'


# Define inputs
parser = argparse.ArgumentParser(description = 'Script to backup data')
parser.add_argument('-i', '--inputFolder', help = 'Name of input folder', required = True)
parser.add_argument('-b', '--backupFolder', help = 'Name of backup folder', required = True)

# Parse inputs
args = parser.parse_args()
inputFolder = args.inputFolder
backupFolder = args.backupFolder

# Backup input folder
dataOps.FileBackup().backup(inputFolder, backupFolder)