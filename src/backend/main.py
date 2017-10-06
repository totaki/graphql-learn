import json
import graphene
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from mutations import Mutations
from store import Store
from query import Query

# Some changes for PR
define("debug", default=True)
define("port", default=10080)


class GraphQLHandler(tornado.web.RequestHandler):

    @property
    def schema(self):
        return self.application.settings['schema']

    @property
    def store(self):
        return self.application.settings['store']

    @property
    def query_data(self):
        body = self.request.body.decode('utf-8')
        content_type = self.request.headers.get_list('Content-Type')[0]
        if 'application/json' in content_type:
            data = json.loads(body)
            query = data['query']
            variables = data.get('variables', None)
            operation_name = data.get('operationName', None)
        else:
            query = body
            variables = None
            operation_name = None
        return query, variables, operation_name

    def get_response(self):
        query, variables, operation_name = self.query_data
        result = self.schema.execute(
            query,
            variable_values=variables,
            context_value={'store': self.store},
            operation_name=operation_name
        )
        self.finish({
            'errors': [e.args for e in result.errors] if result.errors else None,
            'data': result.data
        })

    def get(self):
        self.get_response()

    def post(self):
        self.get_response()


def make_app():
    schema = graphene.Schema(query=Query, mutation=Mutations)
    return tornado.web.Application([
        (r'/graphql', GraphQLHandler),
    ], debug=options.debug, schema=schema, store=Store())


if __name__ == "__main__":
    options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    print(f'Start server listen {options.port}')
    tornado.ioloop.IOLoop.current().start()