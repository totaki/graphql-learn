import os
import yaml
import tornado.ioloop
import tornado.web
from handler import GraphQLHandler
from schema import Schema
from store import JSONStore


CONFIG_FILENAME = 'config.yml'
DEFAULT_CONFIG_FILENAME = 'config_default.yml'


def make_app(config_filename):
    with open(config_filename) as cf:
        config = yaml.load(cf)
    store = JSONStore(['task', 'board'], file_name=config['store'])
    schema = Schema(store=store)
    return tornado.web.Application([
        (r"/graphql", GraphQLHandler),
    ], debug=config['debug'], config=config, schema=schema)


if __name__ == "__main__":
    port = 9999
    config_file = (
        CONFIG_FILENAME
        if os.path.isfile(CONFIG_FILENAME)
        else DEFAULT_CONFIG_FILENAME
    )
    app = make_app(config_file)
    print(f'\nUse {config_file}')
    print(f'Start server listen {port}')
    try:
        app.listen(port)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print(f'Shutdown server')
    except Exception as e:
        print(e)

