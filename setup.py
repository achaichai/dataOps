from setuptools import setup, find_packages
import dataOps

name = 'dataOps'

version = dataOps.__version__

setup(name = name,
      version = version,
      description = 'Data operators to create, update, and backup hierarchical files on disk',
      author = 'James Chryssanthacopoulos',
      author_email = 'jchryssanthacopoulos@gmail.com',
      url = 'https://github.com/jc4089/dataOps',
      scripts = [
        'scripts/generateData.py',
        'scripts/updateData.py',
        'scripts/backupData.py',
        'examples/runGenerateData.sh',
        'examples/runUpdateData.sh',
        'examples/runBackupData.sh',
        'examples/runAll.sh',
        'examples/clean.sh',
        ],
      classifiers = [
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        ],
      packages = find_packages(),
)