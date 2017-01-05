#!/usr/bin/python

"""

Test suite

"""


import unittest
import dataOps
import os
import shutil
import numpy


class DataOpsTestCases(unittest.TestCase):
    """ Tests for dataOps methods """


    def test_write_alphanumeric_file(self):
        # Create temporary directory
        tempDir = 'tempDir'
        if not os.path.exists(tempDir):
            os.makedirs(tempDir)
        
        # Instantiate class object
        cfs = dataOps.ControlledFileSystem(tempDir)
        
        # Create files of different sizes
        for idx, size in enumerate(range(100, 1000000, 10000)):
            filename = os.path.join(tempDir, 'test%03d.txt' % idx)
            cfs._writeAlphanumericBytes(filename, size)
            finalSize = os.path.getsize(filename)
            self.assertTrue(abs(finalSize - size) / numpy.double(size) < 0.05)
        
        # Remove temporary directory
        shutil.rmtree(tempDir)


if __name__ == '__main__':
    unittest.main()