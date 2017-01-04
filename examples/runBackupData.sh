#!/bin/bash

# Add root directory to path
PATH=$PATH:..

# Input folder
inputFolder=exampleData

# Backup folder
backupFolder=backup

# Generate data
backupData.py -i $inputFolder -b $backupFolder