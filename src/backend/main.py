"""
    Application entry point
"""
import tarantool

from contextlib import AbstractContextManager


def get_settings(settings_file='./settings.yml'):
    import yaml
    import os
    file_name = settings_file if os.path.exists(settings_file) else './defaults.yml'
    with open(file_name) as f:
        return yaml.load(f.read())

settings = get_settings()


class SyncTarantoolConnection(AbstractContextManager):

    def __init__(self, host=None, port=None):
        self._connection_args = (host, port)

    @classmethod
    def connect_from_settings(cls):
        return cls(**settings['tarantool'])

    def __enter__(self):
        self._connection = tarantool.connect(*self._connection_args)
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()


def get_connection():
    conn = tarantool.connect(settings['tarantool']['host'], settings['tarantool']['port'])
    return conn


def prepare_db():
    conn = get_connection()
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
    prepare_db()
    _run_command()
