# authors: Andres Pitta, Braden Tam, Serhiy Pokrovskyy
# date: 2020-01-19

'''The script downloads the data file from a URL specified in the DATA_FILE_URL parameter,
verifies its content MD5 checksum with provided DATA_FILE_HASH parameter
and stores it on the local machine at path provided by DATA_FILE_PATH.

Note: Calling the script without the parameters will download the data file to a default location.

Usage: download.py [--DATA_FILE_PATH=<DATA_FILE_PATH>] [--DATA_FILE_URL=<DATA_FILE_URL>] [--DATA_FILE_HASH=<DATA_FILE_HASH>]

Options:
--DATA_FILE_PATH=<DATA_FILE_PATH>  File path (including filename) to save the data file. [default: data/vehicles.csv]
--DATA_FILE_URL=<DATA_FILE_URL>    URL from where to download the dataset. [default: http://mds.dev.synnergia.com/uploads/vehicles.csv]
--DATA_FILE_HASH=<DATA_FILE_HASH>  MD5 checksum hash of the file (for validation). [default: 06e7bd341eebef8e77b088d2d3c54585]
'''

import hashlib
import os
import sys
import urllib.request
from docopt import docopt

opt = docopt(__doc__)


def main(file_path, file_URL, file_hash):
    download_data(file_path, file_URL, file_hash)


def download_data(DATA_FILE_PATH, DATA_FILE_URL, DATA_FILE_HASH=''):
    '''
    Downloads a dataset to a given path from a URL

    Parameters
    --------------
    DATA_FILE_PATH: Local path
    DATA_FILE_URL: Data URL
    DATA_FILE_HASH: Data file checksum hash (default: '')

    Examples
    --------------
    >>> download_data('../data/vehicles.csv', 'http://mds.dev.synnergia.com/uploads/vehicles.csv', '06e7bd341eebef8e77b088d2d3c54585')
    '''
    # Check / download data file
    print("Checking cached data file... ", end='')
    if (os.path.isfile(DATA_FILE_PATH)):
        print("OK")
    else:
        print("NONE")
        urllib.request.urlretrieve(DATA_FILE_URL, DATA_FILE_PATH,
                                   lambda block, block_size, total_size: sys.stdout.write(
                                       "\rDownloading new data file... %.2f%%" %
                                       (round(100.0 * block * block_size / total_size, 2))))
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
        # Hash invalid - delete file and exit
        print("FAIL")
        os.remove(DATA_FILE_PATH)
        print("Cached data file hash is invalid. Please check the URL / hash retry")


if __name__ == "__main__":
    main(opt["--DATA_FILE_PATH"], opt["--DATA_FILE_URL"], opt["--DATA_FILE_HASH"])
