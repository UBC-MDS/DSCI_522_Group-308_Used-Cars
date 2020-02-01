# authors: Andres Pitta, Braden Tam, Serhiy Pokrovskyy
# date: 2020-01-19

'''The script downloads the data file from a URL specified in the --data-file-url parameter,
verifies its content MD5 checksum with provided DATA_FILE_HASH parameter
and stores it on the local machine at path provided by DATA_FILE_PATH.

Note: Calling the script without the parameters will download the data file to a default location.

IMPORTANT: By default, the script downloads a 1.4GB original data file!

Usage: download.py [--DATA_FILE_PATH=<DATA_FILE_PATH>] [--DATA_FILE_URL=<DATA_FILE_URL>] [--DATA_FILE_HASH=<DATA_FILE_HASH>] [--CACHE_OVERRIDE]

Options:
--DATA_FILE_PATH=<DATA_FILE_PATH>  File path (including filename) to save the data file. [default: data/vehicles.csv]
--DATA_FILE_URL=<DATA_FILE_URL>    URL from where to download the dataset. [default: http://mds.dev.synnergia.com/uploads/vehicles.csv]
--DATA_FILE_HASH=<DATA_FILE_HASH>  MD5 checksum hash of the file (for validation). [default: 06e7bd341eebef8e77b088d2d3c54585]
--CACHE_OVERRIDE                   Force override data file cache
'''

import hashlib
import os
import sys
import urllib.request
from docopt import docopt

opt = docopt(__doc__)


def main(data_file_path, data_file_url, data_file_hash=None, cache_override=False):
    """
    Main entry for the data download script.

    Arguments
    ---------
    data_file_path : str
        File path (including filename) to save the data file.
    data_file_url : str
        URL from where to download the dataset.
    data_file_hash : str
        Optional MD5 hash to validate the downloaded file. (Default = None)
    cache_override : int
        Whether to override the cached file if it exists (Default = False)
    """

    # Check / download data file
    print("Checking cached data file... ", end='')
    if not cache_override and os.path.isfile(data_file_path):
        print("OK")
    else:
        print("SKIPPED" if cache_override else "NONE")
        urllib.request.urlretrieve(data_file_url, data_file_path,
                                   lambda block, block_size, total_size: sys.stdout.write(
                                       "\rDownloading new data file... %.2f%% of %.2f MB" %
                                       (round(100.0 * block * block_size / total_size, 2), total_size / (2 ** 20))))
        print("DONE")

    # Validate downloaded data file hash
    print("Validating data file hash... ", end='')
    if data_file_hash:
        hasher = hashlib.md5()
        with open(data_file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(1024 * 1024 * 256), ""):
                if len(chunk) == 0:
                    break;
                hasher.update(chunk)

    if not data_file_hash or hasher.hexdigest() == data_file_hash:
        print("OK" if data_file_hash else 'SKIPPED')
        print("SUCCESS - data file available at", data_file_path)
    else:
        # Hash invalid - delete file and exit
        print("FAIL")
        os.remove(data_file_path)
        print("Cached data file hash is invalid (deleted). Please check the URL / hash and retry")


if __name__ == "__main__":
    main(opt["--DATA_FILE_PATH"],
         opt["--DATA_FILE_URL"],
         opt["--DATA_FILE_HASH"],
         opt["--CACHE_OVERRIDE"])
