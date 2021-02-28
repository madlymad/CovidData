import sys
import os
import os.path
from os import path
import yaml
from util import resource_path

KEY_VIBER_NO = "viberNO"
KEY_VIBER_DB = "viberDB"


def configFilename():
    return resource_path("config.yaml")


def viberDbPath(number: str):
    viberPC = os.path.join(os.environ['APPDATA'], "ViberPC")
    viberDb = os.path.join(viberPC, number, "viber.db")
    return viberDb


def _initConfig():
    config = {}

    print("Please type your viber number eg. 3069XXXXXXXX:", end=' ')
    message = input()
    if message:
        config[KEY_VIBER_NO] = message

    config = configDB(config)

    saveConfig(config)
    return config


def saveConfig(config):
    with open(configFilename(), 'w') as f:
        yaml.dump(config, stream=f,
                  default_flow_style=False, sort_keys=False)
        print(f"Configuration saved at {configFilename()}")


def verifyDb(message, config):
    if not message:
        config[KEY_VIBER_DB] = viberDbPath(config[KEY_VIBER_NO])
    else:
        config[KEY_VIBER_DB] = message
    if path.exists(config[KEY_VIBER_DB]):
        return True, config
    else:
        return False, config


def configDB(config):
    while True:
        print(
            f"Set ViberDb location.\nDefault \"{viberDbPath(config[KEY_VIBER_NO])}\":", end=' ')
        message = input()
        valid, config = verifyDb(message, config)
        if valid:
            break
        else:
            print("Please enter a valid path or leave empty to get the default.")
    return config


def readConfig():
    config = {}
    if not path.exists(configFilename()):
        return config
    with open(configFilename(), 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config


def hasConfig():
    config = readConfig()
    exist = True
    if not KEY_VIBER_NO in config:
        exist = False
    if not KEY_VIBER_DB in config:
        exist = False
    if exist:
        print(f"Configuration retrieved from {configFilename()}")
    return exist


def initConfig():
    configured = hasConfig()
    if not configured:
        _initConfig()
    config = readConfig()
    if configured:
        valid, config = verifyDb(config[KEY_VIBER_DB], config)
        if not valid:
            configDB(config)
            saveConfig(config)

    return config
