import tornado.web
from schema import schema


class GraphQLHandler(tornado.web.RequestHandler):

    def post(self):
        result = schema.execute('''
            query {
                hello
            }
        ''')
        if result.errors:
            self.write({'errors': [e.args for e in result.errors]})
        else:
            self.write(result.data)
