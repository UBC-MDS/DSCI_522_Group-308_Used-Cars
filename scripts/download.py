# authors: Andres Pitta, Braden Tam, Serhiy Pokrovskyy
# date: 2020-01-19

'''This scripts uploads the data directly from an url and downloads it in 
your local machine.

Usage: download.py [--DATA_FILE_PATH=<DATA_FILE_PATH>] [--DATA_FILE_URL=<DATA_FILE_URL>]

Options:
--DATA_FILE_PATH=<DATA_FILE_PATH>  Path (including filename) to print the csv file. [default: ../data/vehicles.csv]
--DATA_FILE_URL=<DATA_FILE_URL>  URL from where to extract the dataset. [default: http://mds.dev.synnergia.com/uploads/vehicles.csv]
'''

import hashlib
import os
import urllib.request
from docopt import docopt

opt = docopt(__doc__)

# Define constants with key values
#DATA_FILE_PATH = '../data/vehicles.csv'
DATA_FILE_HASH = '06e7bd341eebef8e77b088d2d3c54585'
#DATA_FILE_URL = 'http://mds.dev.synnergia.com/uploads/vehicles.csv'

def main(file_path, file_URL):
    download_data(file_path, file_URL)

def download_data(DATA_FILE_PATH, DATA_FILE_URL):
    '''
    Downloads a dataset to a given path from a URL

    Parameters
    --------------
    DATA_FILE_PATH: Local path

    DATA_FILE_URL: Data URL

    Examples
    --------------
    >>> download_data('../data/vehicles.csv', 'http://mds.dev.synnergia.com/uploads/vehicles.csv')
    '''
    # Check / download data file
    print("Checking cached data file... ", end='')
    if (os.path.isfile(DATA_FILE_PATH)):
        print("OK")
    else:
        print("NONE")
        print("Downloading new data file... ", end='')
        urllib.request.urlretrieve(DATA_FILE_URL, DATA_FILE_PATH)
        print("DONE")

    # Validate downloaded data file hash
    print("Validating data file hash... ", end='')
    hasher = hashlib.md5()
    with open(DATA_FILE_PATH, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024 * 256), ""):
            if len(chunk) == 0:
                break;
            hasher.update(chunk)
    if hasher.hexdigest() == DATA_FILE_HASH:
        print("OK")
        print("SUCCESS - valid data file available at", DATA_FILE_PATH)
    else:
        # Hash invalid - download file and exit
        print("FAIL")
        os.remove(DATA_FILE_PATH)
        print("Cached data file hash is invalid")

if __name__ == "__main__":
    main(opt["--DATA_FILE_PATH"], opt["--DATA_FILE_URL"])