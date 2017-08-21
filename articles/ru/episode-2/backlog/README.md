[Назад](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/README.md#get-backlog)|
-----|

Для создания resolver, мы должны в наш класс добавить метод ```resolve_{{ field name }}```. При в него передаются 3
дополнительных аргумента.
1. args, параметры которые мы передали в запросе ```query_field(arg_1: value_1, arg_2: value_2)```
2. context, то что мы передади в наш executor, это может подключение к БД или данные авторизации, они передаются между запросами.
```TODO: проверить можем ли мы изменять контекст, чтобы он передавался измененный между запросами.``` 
3. info, тут можно найти, сам запрос, структуру нашего объекта и много другой мета информации 

Так же можно передать в наше поле resolver явно.

```python

def resolver(root, args, context, info):
    return 'Hello world'

class Query(graphene.ObjectType):
    reverse = graphene.String(resolver=resolver)
```

Касательно нашего приложения, то в backlog попадают все таски у которых отсутствует ```iteration_id```

[query.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/query.py)

```python
class Query(graphene.ObjectType):

    backlog_description = '''
    This field include all tasks without iteration
    '''
    backlog = graphene.List(
        TaskObject, description=backlog_description
    )

    def resolve_backlog(self, args, context, info):
        tasks = context['store'].tasks
        return [
            TaskObject(**task.as_dict)
            for task in filter(lambda t: not t.iteration_id, tasks)
        ]
```

В результате мы можем выполнить [запрос](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/backlog/query.graphql)

![Backlog](https://raw.githubusercontent.com/totaki/graphql-learn/develop/articles/ru/episode-2/backlog/getBacklog.gif)