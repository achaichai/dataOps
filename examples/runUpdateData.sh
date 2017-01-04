#!/bin/bash

# Add root directory to path
PATH=$PATH:..

# Input folder
inputFolder=exampleData

# Subfolder names and sizes
folders=location,12,sensors,23,devices,10

# Generate data
updateData.py -i $inputFolder -f $folders