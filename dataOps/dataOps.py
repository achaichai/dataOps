'''
    File name: dataOps.py
    Author: James Chryssanthacopoulos
    Date created: 01/03/2017
    Date last modified: 01/04/2017
'''


# Load modules
import string
import os
import random
import shutil
import filecmp
from os.path import join as pjoin
from os import listdir as ldir


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
        Class constructor:
            ControlledFileSystem(directory, targetFileSize, targetDirSize)
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
        """
        This method returns the size of the directory in bytes
        """
        dirListing = ldir(self.directory)
        
        dirSize = 0
        for item in dirListing:
            itemFullPath = pjoin(self.directory, item)
            
            if os.path.isfile(itemFullPath):
                dirSize += os.path.getsize(itemFullPath)
        
        return dirSize
    
    
    def _numFiles(self):
        """
        This method returns the number of files in the directory
        """
        return len(ldir(self.directory))


    def _fileFull(self, fileSize):
        """
        This method checks if the size of the file is within 1% of the target size or more
        """
        return fileSize >= 0.99 * self.targetFileSize
    
    
    def _dirFull(self):
        """
        This method checks if the size of the directory is within 1% of the target size or more or if the max file number has been reached
        """
        return self._dirSize() >= 0.99 * self.targetDirSize or self._numFiles() >= self.maxFiles



# This class generates a random master dataset as a set of files on disk
class DataInitializer(ControlledFileSystem):
    def __init__(self, directory, targetFileSize, targetDirSize):
        super(DataInitializer, self).__init__(directory, targetFileSize, targetDirSize)
        """
        Class constructor:
            DataInitializer(directory, targetFileSize, targetDirSize)
        """        
        # Make directory if it doesn't already exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            # Remove any preexisting files
            filelist = ldir(directory)
            for filename in filelist:
                os.remove(pjoin(directory, filename))
    
    
    def writeData(self):
        """
        This method creates all files in the directory according to the specifications
        """
        
        print 'Writing data for directory %s . . .' % self.directory
        
        # Keep creating files until directory size has reached the target
        # or if maximum number of files has been reached
        
        while not self._dirFull():
            # Get new filename of file to write
            filename = pjoin(self.directory, 'file%02d.txt' % (self._numFiles() + 1))
            
            # Write file
            self.writeFile(filename)



# This class updates a master dataset
class DataUpdater(ControlledFileSystem):    
    def __init__(self, directory, targetFileSize, targetDirDelta):
        """
        Class constructor:
            DataUpdater(directory, targetFileSize, targetDirDelta)
        """
        super(DataUpdater, self).__init__(directory, targetFileSize)
        
        # Set dtarget directory size to current size plus delta
        self.targetDirSize = self._dirSize() + targetDirDelta


    def updateData(self):
        """
        This method updates all files in the directory according to the specifications
        """
        
        print 'Updating data for directory %s . . .' % self.directory
        
        # Keep creating files until directory size has reached the target
        # or if maximum number of files has been reached
        
        # Update last file if need be
        lastCreatedFile = pjoin(self.directory, ldir(self.directory)[-1])
        self.writeFile(lastCreatedFile)
        
        while not self._dirFull():
            # Get new filename of file to write
            filename = pjoin(self.directory, 'file%02d.txt' % (self._numFiles() + 1))
            
            # Write file
            self.writeFile(filename)



# This class backups a master dataset
class DataBackup(object):
    """
    DataBackup()
    """
    
    def backup(self, dataDirectory, backupDirectory):
        """
        This method backups a master dataset into a backup directory
        """
        
        print 'Backing up directory %s into %s . . .' % (dataDirectory, backupDirectory)
        
        # Name of directory
        dataName = os.path.basename(dataDirectory)
        
        # Name in backup directory
        backupName = pjoin(backupDirectory, dataName)
        
        # Create directory in backup if it doesn't exist
        if not os.path.exists(backupName):
            os.makedirs(backupName)
        
        # List of subdirectories
        srcDirNames = ldir(dataDirectory)
        
        # Remove stale subdirectories in backup
        for d in [drct for drct in ldir(backupName) if drct not in srcDirNames]:
            shutil.rmtree(pjoin(backupName, d))
        
        # Iterate through subdirectories
        for dirName in srcDirNames:
            srcDirName = pjoin(dataDirectory, dirName)
            destDirName = pjoin(backupName, dirName)
            
            # Create subdirectory if it doesn't exist
            if not os.path.exists(destDirName):
                os.makedirs(destDirName)
            
            # List of files
            srcFiles = ldir(srcDirName)
            
            # Remove stale files in backup
            for f in [fname for fname in ldir(destDirName) if fname not in srcFiles]:
                os.remove(pjoin(destDirName, f))
            
            # Iterate through files
            for fileName in srcFiles:
                srcFileName = pjoin(srcDirName, fileName)
                destFileName = pjoin(destDirName, fileName)
                
                # Copy file if it doesn't exist in backup or a different file of the same name resides there
                if not os.path.exists(destFileName) or not filecmp.cmp(srcFileName, destFileName):
                    shutil.copyfile(srcFileName, destFileName)