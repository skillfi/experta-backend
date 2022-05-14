import logging
import os
import configparser

CONFIG_FILE_NAME = 'config.ini'
CONFIG_SETTINGS_SECTION_NAME = 'settings'

option_default_list = {
    'DEBUG': 0,
    'HTTP_PORT': 38080,
    'DB_USERNAME': None,
    'DB_PASSWORD': None,
    'DB_HOST': 'cluster0.ftcyu.mongodb.net',
    'DB_NAME': 'ES'
}


def determine_config(option, read_in_config, default):
    try:
        if read_in_config.get(option):
            return read_in_config[option]
        elif option in os.environ:
            return os.environ[option]
        else:
            return default
    except Exception as ex:
        logging.error(f'Failed to determine config {option}, {ex}')
        return default


def get_configs():
    ini_config = configparser.ConfigParser()
    ini_config.read(CONFIG_FILE_NAME)
    if CONFIG_SETTINGS_SECTION_NAME in ini_config.sections():
        read_in_config = ini_config[CONFIG_SETTINGS_SECTION_NAME]
    else:
        read_in_config = {}
    config = {}
    for option in option_default_list:
        config[option] = determine_config(option, read_in_config, None)

    return config
