# dataOps
dataOps is a Python package for generating, updating, and backing up datasets represented as sets of files on disk.

# How to Install
The package can be installed by downloading the source code and running

`pip install -r requirements.txt`

within a virtual environment or, alternatively, using setup.py:

`python setup.py install`

# How to Use
The package contains three data operations: generate, update, and backup. To generate a master dataset, run:

`generateData.py [--help] -i INPUTFOLDER -s FILESIZE -f FOLDERS`

where `INPUTFOLDER` is the location to write to, `FILESIZE` is approximately file size of each file in megabytes (except potentially the last), and `FOLDERS` is a list of subfolder names and sizes in MB in the form of `<name1>,<size1>,<name2>,<size2>,...`.

Similarly, to update a master dataset, run:

`updateData.py [--help] -i INPUTFOLDER -f FOLDERS`

where `INPUTFOLDER` is the dataset to update and `FOLDERS` is a list of folder names and sizes in MB to increase by in the same form as before.

Finally, a dataset is backed up using:

`backupData.py [--help] -i INPUTFOLDER -b BACKUPFOLDER`

where `INPUTFOLDER` and `BACKUPFOLDER` are the input and backup folders, respectively.

These utilities can also be run with example options using `runGenerateData.sh`, `runUpdateData.sh`, and `runBackupData.sh`. An example master script calling all of these utilities in a processing chain can be run with `runAll.sh`.

Enjoy!
