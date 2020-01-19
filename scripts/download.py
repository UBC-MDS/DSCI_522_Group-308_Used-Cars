import hashlib
import os
import urllib.request

# Define constants with key values
DATA_FILE_PATH = '../data/vehicles.csv'
DATA_FILE_HASH = '06e7bd341eebef8e77b088d2d3c54585'
DATA_FILE_URL = 'http://mds.dev.synnergia.com/uploads/vehicles.csv'

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
    # os.remove(DATA_FILE_PATH)
    print("Cached data file hash is invalid")
