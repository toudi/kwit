import os.path
from os import mkdir
from configparser import SafeConfigParser

config_base_dir = os.path.expanduser('~/.kwit/')
config_file = os.path.join(config_base_dir, 'kwit.ini')

config = SafeConfigParser()

if not os.path.exists(config_base_dir):
    mkdir(config_base_dir)

config.read(config_file)


def get(key, default=None, expanduser=True):
    if 'kwit' not in config:
        config['kwit'] = {}
    if not config.has_option('kwit', key):
        if '~' in default and expanduser:
            default = default.replace('~', os.path.expanduser('~'))
        config.set('kwit', key, default)
    return config.get('kwit', key)


def get_array(key, default):
    # chcemy pobrac tablice na zewnatrz, ale jednoczesnie chcemy
    # zeby do settingsow zapisala sie wartosc z przecinkami
    # (jesli ustawienia nie ma i przekazujemy defaulta.)
    return get(key, ','.join(default)).split(',')


def set_array(key, value):
    config.set('kwit', key, ','.join(value))


def save():
    with open(config_file, 'w') as fp:
        config.write(fp)
