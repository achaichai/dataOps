'''
    File name: dataOperators.py
    Author: James Chryssanthacopoulos
    Date created: 01/03/2017
    Date last modified: 01/03/2017
    Python Version: 2.7
'''


# Load modules
import string
import os
import random


# This class generates a random master dataset as a set of files on disk
class FileInitializer:  
    # Maximum number of bytes in each line
    maxBytesPerLine = 100
    
    # The following are to provide a safeguard from the directory becoming too big
    maxFiles = 1000         # Maximum number of files to write
    maxLinesPerFile = 10000 # Maximum number of lines per file
    
    # Complete alphanumeric set
    alphanumericSet = string.ascii_letters + string.digits
    
    
    def __init__(self, directory, fileSize, directorySize):
        """
        Class constructor
        """
        
        # Initialize member variables
        self.directory     = directory
        self.fileSize      = fileSize
        self.directorySize = directorySize
        
        # Make directory if it doesn't already exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            # Remove any preexisting files
            filelist = os.listdir(directory)
            for filename in filelist:
                os.remove(os.path.join(directory, filename))

        # Current directory size in bytes and number of files        
        self.currentDirectorySize = 0
        self.numFiles = 0
    
    
    def writeFiles(self):
        """
        This method will create all the files in the directory
        according to the specifications
        """
        
        # Keep creating files until directory size has reached the target
        # or if maximum number of files has been reached
        
        while not self._directoryFull() and self.numFiles < self.maxFiles:
            # Get new filename of file to write
            filename = os.path.join(self.directory, 'file{}.txt'.format(self.numFiles + 1))
            
            # Write file
            self._writeFile(filename)
            
            # Increment number of files
            self.numFiles += 1
    
    
    def _writeFile(self, filename):
        """ 
        This method will write a new file with an appropriate size
        """

        # File size counter
        currentFileSize = 0
        
        # Number of lines counter
        numLines = 0
        
        # Write file
        with open(filename, 'w') as f:
            # Keep writing new lines of randomly generated strings of alphanumeric characters
            # of varying sizes until the file size or directory sizes have reached their targets
            # or maximum number of lines has been reached
            
            while not self._fileFull(currentFileSize) and not self._dirFull() and numLines < self.maxLinesPerFile:
                # Number of bytes to write assuming each character is one byte
                numBytes = random.randrange(1, self.maxBytesPerLine)
                
                # Generate line
                line = ''.join([random.choice(self.alphaNumericSet) for n in range(numBytes)])
                
                # Write line to end of file
                f.write('{}\n'.format(line))
                
                # Increment file size
                currentFileSize += numBytes + 2 # newline counts for two
                
                # Increment directory size
                self.currentDirectorySize += numBytes + 2
                
                # Increment number of lines in file
                numLines += 1
    
    
    def _fileFull(self, fileSize):
        """
        This method checks if the size of the file is within 5% of the target size
        """
        return abs(fileSize - self.fileSize) < 0.05 * self.fileSize
    
    
    def _dirFull(self):
        """
        This method checks if the size of the directory is within 5% of the target size
        """
        return abs(self.currentDirectorySize - self.directorySize) < 0.05 * self.directorySize