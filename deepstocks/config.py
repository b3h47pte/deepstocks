#
# Read configuration from disk.
#

import appdirs
import os
import json

# CONFIG KEYS
kAlphaVantageConfigKey = 'ALPHA_VANTAGE_KEY'

defaultConfig = {
    kAlphaVantageConfigKey: 'NEEDS_TO_BE_REPLACED'
}

def readConfigFromDisk():
    configDir = appdirs.user_config_dir(appname='Deepstocks')
    os.makedirs(configDir, exist_ok=True)

    configFname = os.path.join(configDir, 'config.json')
    if not os.path.exists(configFname):
        config = dict(defaultConfig)
        with open(configFname, 'w') as f:
            json.dump(config, f)
        return config

    with open(configFname, 'r') as f:
        return json.load(f)

_config = readConfigFromDisk()

def getConfigValue(key):
    return _config[key]
