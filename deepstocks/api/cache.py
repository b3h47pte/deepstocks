#
# Cache API calls on disk.
#

import appdirs
import hashlib
import os
import json

dataDir = os.path.join(appdirs.user_data_dir(), 'Deepstocks')
os.makedirs(dataDir, exist_ok=True)

def getCachedResponse(url):
    m = hashlib.sha256(url.encode('utf-8')).hexdigest()
    
    fname = os.path.join(dataDir, m + '.json')
    if not os.path.exists(fname):
        return None

    with open(fname, 'r') as f:
        return json.load(f)

def storeCachedResponse(url, resp):
    m = hashlib.sha256(url.encode('utf-8')).hexdigest()
    
    fname = os.path.join(dataDir, m + '.json')
    with open(fname, 'w') as f:
        json.dump(resp, f)
