from setuptools import setup, find_packages
import dataOperators

name = 'dataOperators'

version = dataOperators.__version__

setup(name = name,
      version = version,
      description = 'Data operators to create, update, and backup hierarchical files on disk',
      author = 'James Chryssanthacopoulos',
      author_email = 'jchryssanthacopoulos@gmail.com',
      url = 'https://github.com/marcelcaraciolo/foursquare',
      download_url = 'https://github.com/marcelcaraciolo/foursquare/tarball/master',
      classifiers = [
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        ],
      packages = find_packages(),
)