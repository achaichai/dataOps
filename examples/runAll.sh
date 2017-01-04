#!/bin/bash

# Add root directory to path
PATH=$PATH:..

################
## PARAMETERS ##
################

# Input folder
inputFolder=exampleData

# Backup folder
backupFolder=backup

# Individual file size in MB
fileSize=10

# Subfolder names and sizes
folders=location,64,sensors,138,devices,24

# Subfolder names and increments
incFolders=location,12,sensors,23,devices,10

###################
## GENERATE DATA ##
###################

echo GENERATING DATA ...
generateData.py -i $inputFolder -s $fileSize -f $folders

#################
## BACKUP DATA ##
#################

echo BACKINGUP DATA ...
backupData.py -i $inputFolder -b $backupFolder

#################
## UPDATE DATA ##
#################

echo UPDATING DATA ...
updateData.py -i $inputFolder -f $incFolders

#########################
## BACKUP UPDATED DATA ##
#########################

echo BACKING UP UPDATED DATA ...
backupData.py -i $inputFolder -b $backupFolder

#################
## CLEANING UP ##
#################

rm -rf $inputFolder