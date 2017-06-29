import tornado.ioloop
import tornado.web

from handler import GraphQLHandler


def make_app():
    return tornado.web.Application([
        (r"/graphql", GraphQLHandler),
    ], debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(9999)
    tornado.ioloop.IOLoop.current().start()