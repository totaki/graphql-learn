import json
import graphene
import tornado.ioloop
import tornado.web
from tornado.options import define, options

define("debug", default=True)
define("port", default=8888)


class Query(graphene.ObjectType):
    hello = graphene.String(description='some')

    def resolve_hello(self, args, context, info):
        return 'World'


class GraphQLHandler(tornado.web.RequestHandler):

    @property
    def schema(self):
        return self.application.settings['schema']

    @property
    def query_data(self):
        body = self.request.body.decode('utf-8')
        content_type = self.request.headers.get_list('Content-Type')[0]
        if content_type == 'application/json':
            data = json.loads(body)
            query = data['query']
            variables = data.get('variables', None)
        else:
            query = body
            variables = None
        return query, variables

    def get_response(self):
        query, variables = self.query_data
        result = self.schema.execute(query, variable_values=variables)
        self.finish({
            'errors': result.errors,
            'data': result.data
        })

    def get(self):
        self.get_response()

    def post(self):
        self.get_response()


def make_app():
    schema = graphene.Schema(query=Query)
    return tornado.web.Application([
        (r'/graphql', GraphQLHandler),
    ], debug=options.debug, schema=schema)


if __name__ == "__main__":
    options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    print(f'Start server listen {options.port}')
    tornado.ioloop.IOLoop.current().start()