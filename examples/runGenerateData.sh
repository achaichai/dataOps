#!/bin/bash

# Add root directory to path
PATH=$PATH:..

# Input folder
inputFolder=exampleData

# Individual file size in MB
fileSize=10

# Subfolder names and sizes
folders=location,64,sensors,138,devices,24

# Generate data
generateData.py -i $inputFolder -s $fileSize -f $folders