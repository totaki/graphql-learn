import tornado.web


class GraphQLHandler(tornado.web.RequestHandler):

    @property
    def schema(self):
        return self.application.settings['schema']

    @property
    def query(self):
        return self.request.body.decode('utf-8')

    def post(self):
        result = self.schema.execute(self.query)
        self.set_header('Access-Control-Allow-Origin', '*')
        if result.errors:
            self.write({'errors': [e.args for e in result.errors]})
        else:
            self.write(result.data)
