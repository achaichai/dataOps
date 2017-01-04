'''
    File name: dataOperators.py
    Author: James Chryssanthacopoulos
    Date created: 01/03/2017
    Date last modified: 01/04/2017
    Python Version: 2.7
'''


# Load modules
import string
import os
import random


# Superclass
class ControlledFileSystem(object):
    # Maximum number of bytes in each line (should probably make this relative to targetFileSize?)
    maxBytesPerLine = 10000
    
    # Maximum number of lines allowed per file to provide a safeguard from file becoming too big
    maxLinesPerFile = 1e5
    
    # Maximum number of files allowed in the directory to provide a safeguard from the directory becoming too big
    maxFiles = 1000
    
    # Complete alphanumeric set
    alphanumericSet = string.ascii_letters + string.digits
    
    
    def __init__(self, directory, targetFileSize = 0, targetDirSize = 0):
        """
        Class constructor: ControlledFileSystem(directory, targetFileSize, targetDirSize)
        """
        self.directory = directory
        self.targetFileSize = targetFileSize
        self.targetDirSize = targetDirSize


    def writeFile(self, filename):
        """
        Write a new file or update existing file while satisfying targets
        """
        # Exit if directory is already full
        if self._dirFull():
            return
        
        # Get size of file in bytes
        currentFileSize = os.path.getsize(filename) if os.path.exists(filename) else 0
        
        # Exit if file is already full
        if self._fileFull(currentFileSize):
            return
        
        # Number of bytes to write into file
        fileDelta = self.targetFileSize - currentFileSize # Guaranteed to be positive
        dirDelta = self.targetDirSize - self._dirSize()
        numBytes = min(fileDelta, dirDelta)
        
        # Write file
        self._writeAlphanumericBytes(filename, numBytes)


    def _writeAlphanumericBytes(self, filename, numBytes):
        """
        This method writes random lines of randomly generated strings of
        alphanumeric characters of varying sizes into a file
        """
        # Generate data
        data = ''.join([random.choice(self.alphanumericSet) for n in range(numBytes)])

        # Write to file
        with open(filename, 'a') as f:
            BytesWritten = 0
            numLines = 0
            
            while BytesWritten < numBytes and numLines < self.maxLinesPerFile:
                numBytesPerLine = random.randrange(1, self.maxBytesPerLine + 1)
                
                print >> f, data[BytesWritten : BytesWritten + numBytesPerLine]
                
                BytesWritten += numBytesPerLine
                
                numLines += 1


    def _dirSize(self):
        dirListing = os.listdir(self.directory)
        
        dirSize = 0
        for item in dirListing:
            itemFullPath = os.path.join(self.directory, item)
            
            if os.path.isfile(itemFullPath):
                dirSize += os.path.getsize(itemFullPath)
        
        return dirSize
    
    
    def _numFiles(self):
        return len(os.listdir(self.directory))


    def _fileFull(self, fileSize):
        """
        This method checks if the size of the file is within 1% of the target size or more
        """
        return fileSize >= 0.99 * self.targetFileSize
    
    
    def _dirFull(self):
        """
        This method checks if the size of the directory is within 1% of the target size or more
        """
        return self._dirSize() >= 0.99 * self.targetDirSize or self._numFiles() >= self.maxFiles



# This class generates a random master dataset as a set of files on disk
class FileInitializer(ControlledFileSystem):
    def __init__(self, directory, targetFileSize, targetDirSize):
        super(FileInitializer, self).__init__(directory, targetFileSize, targetDirSize)
        """
        Class constructor
        """        
        # Make directory if it doesn't already exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            # Remove any preexisting files
            filelist = os.listdir(directory)
            for filename in filelist:
                os.remove(os.path.join(directory, filename))
    
    
    def writeFiles(self):
        """
        This method will create all the files in the directory according to the specifications
        """
        
        print 'Writing files for directory %s . . .' % self.directory
        
        # Keep creating files until directory size has reached the target
        # or if maximum number of files has been reached
        
        while not self._dirFull():
            # Get new filename of file to write
            filename = os.path.join(self.directory, 'file%02d.txt' % (self._numFiles() + 1))
            
            # Write file
            self.writeFile(filename)



# This class updates a master dataset
class FileUpdater(ControlledFileSystem):    
    def __init__(self, directory, targetFileSize, targetDirDelta):
        super(FileUpdater, self).__init__(directory, targetFileSize)
        
        # Set dtarget directory size to current size plus delta
        self.targetDirSize = self._dirSize() + targetDirDelta


    def updateFiles(self):
        """
        This method will update all the files in the directory according to the specifications
        """
        
        print 'Updating files for directory %s . . .' % self.directory
        
        # Keep creating files until directory size has reached the target
        # or if maximum number of files has been reached
        
        # Update last file if need be
        lastCreatedFile = os.path.join(self.directory, os.listdir(self.directory)[-1])
        self.writeFile(lastCreatedFile)
        
        while not self._dirFull():
            # Get new filename of file to write
            filename = os.path.join(self.directory, 'file%02d.txt' % (self._numFiles() + 1))
            
            # Write file
            self.writeFile(filename)        