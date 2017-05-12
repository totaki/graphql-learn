"""
    Application entry point
"""

def _run_command():
    import importlib
    import sys
    command = importlib.import_module('commands.%s' % sys.argv[1])
    command.run()


if __name__ == '__main__':
    _run_command()
