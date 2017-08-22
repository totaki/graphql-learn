[Назад](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/README.md#get-dashboard)|
-----|

В [graphQL](http://graphql.org/) мы можем передать в конструктор наши поля, либо
вычислить их когда нам надо. Тут есть важный момент, надо поля которые используются
при вычисленеиях передавать в конструктор. ```TODO: надо точно все проверить```. В нашем
случае у запиши в БД итерации имеется только дата начала итерации, дату окончания
мы вычисляем, если это нам надо. Также мы передаем смещение относительно даты.


[object_types/iteratin.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/object_types/iteratin.py)

```python
class IterationObject(graphene.ObjectType):
    id = graphene.Int()
    start_date = DateTime()
    tasks = graphene.List(TaskObject)
    end_date = DateTime()

    def resolve_tasks(self, args, context, info):
        result = []
        if self.id:
            tasks = context['store'].tasks
            result.extend([
                TaskObject(**task.as_dict)
                for task
                in filter(lambda t: t.iteration_id == self.id, tasks)
            ])
        return result

    def resolve_end_date(self, args, context, info):
        return self.start_date + dt.timedelta(days=6)
```

[query.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/query.py)

```python
from utils import get_iteration_datetime


class Query(graphene.ObjectType):
   
    ...
    
    dashboard = graphene.Field(
        IterationObject,
        iteration_id=graphene.Int(),
        offset=graphene.Int()
    )

    ...

    def resolve_dashboard(self, args, context, info):
        iteration_dt = get_iteration_datetime(args)
        iterations = context['store'].iterations
        filtered_iterations = list(filter(lambda i: i.start_date == iteration_dt, iterations))
        if filtered_iterations:
            return IterationObject(**filtered_iterations[0].as_dict)
        else:
            return IterationObject(id=None, start_date=iteration_dt)
```
В [GraphiQL](https://github.com/graphql/graphiql), есть возможность передать выполненные вами запросы как ссылку или
аргумент запроса ```query```, если вы нашли баг или ошибку и вам надо передать это дела разработчик, очень удобно.
Так же если вы дали имена ваiим запросам, можно разместить их в одном поле ввода [GraphiQL](https://github.com/graphql/graphiql)
и вызывать по имени.

В результате мы можем выполнить [запрос](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/dashboard/query.graphql)

![Dashboard](https://raw.githubusercontent.com/totaki/graphql-learn/develop/articles/ru/episode-2/dashboard/getDashboard.gif)
