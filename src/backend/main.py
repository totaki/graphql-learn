"""
    Application entry point
"""


def get_settings(settings_file='./settings.yml'):
    import yaml
    import os
    file_name = settings_file if os.path.exists(settings_file) else './defaults.yml'
    with open(file_name) as f:
        return yaml.load(f.read())

settings = get_settings()


def prepare_db(tarantool_settings):
    import tarantool
    conn = tarantool.connect(tarantool_settings['host'], tarantool_settings['port'])
    with open('./db_scripts/init.lua') as f:
        execution = f.read()
    conn.eval(execution)
    conn.close()


def _run_command():
    import importlib
    import sys
    command = importlib.import_module('commands.%s' % sys.argv[1])
    command.run()


if __name__ == '__main__':
    prepare_db(settings['tarantool'])
    _run_command()
