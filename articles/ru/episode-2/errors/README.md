[Назад](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/README.md#errors)|
-----|

Все что надо нам сделать, так это вернуть объект ```graphql.GraphQLError```.

[query.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/query.py)
```python
from graphql import GraphQLError


class Query(graphene.ObjectType):

    ...
    
    error = graphene.String()

    ...

    def resolve_error(self, *args):
        return GraphQLError('Custom application error')
```

В результате мы можем выполнить [запрос](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/errors/query.graphql)

![Errors](https://raw.githubusercontent.com/totaki/graphql-learn/develop/articles/ru/episode-2/errors/errors.gif)
