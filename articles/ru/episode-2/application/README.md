[Назад]()|
-----|

Для обработки входящих запросов мы будем использовать **tornado**, у которого будет один единственный обработчик. Тут есть пара моментов
не указанных в документации. Когда я писал через тесты то передавал просто **query** в теле запроса, как строку (пример ```query { hello }```),
в последтвии когда подключил **GraphiQL**, увидел что там прилетает ```application/json``` и он в себя уже включает несколько полей, это **query** (сам запрос),
**variables** (опционально, переменные запроса, это объект) и **operationName** (опционально, название запроса, ```query helloQuery { hello }```). Мы получаем эти поля и передаем в наш
executor.

[query.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/query.py)
```python
import graphene

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, args, context, info):
        return 'World'
```


[main.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/main.py)

```python
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
```

В резултате мы можем выполнить [запрос](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/application/query.graphql)

![Create tasks](https://raw.githubusercontent.com/totaki/graphql-learn/develop/articles/ru/episode-2/application/helloQuery.gif)

Отличительной особеностью GraphQL и его реализаций, является самодокументация
нашего API. В нашем случае я использую GraphiQL, он как в последствии
оказались в PyCharm можно поставить плагин и настроить его для получения
нашей схемы с сервера, пример можно посмотреть в репозитарии
[graphql.config.json](https://github.com/totaki/graphql-learn/blob/develop/graphql.config.json)

![Create tasks](https://raw.githubusercontent.com/totaki/graphql-learn/develop/articles/ru/episode-2/application/docHello.gif) 
 