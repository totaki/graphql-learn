[Назад](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/README.md#create-tasks)|
-----|

Для начала давайте создадим класс для наших задач. Только разобьем его на
несколько компонентов. Первые два ```TaskFields``` и ```TaskObject```, являющейся подклассом
[graphene.AbstractType](http://docs.graphene-python.org/en/latest/types/abstracttypes/),
данный абстаркный класс отсутствует в [спецификации](http://facebook.github.io/graphql/)
и является реализацией [graphene](http://graphene-python.org/).
[graphene.AbstractType](http://docs.graphene-python.org/en/latest/types/abstracttypes/) позволяет
не дублировать поля у родственных классов. Также добавим статус для наших задача,
который является подклассом [graphene.Enum](http://docs.graphene-python.org/en/latest/types/enums/)

[enums/task_status.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/enums/task_status.py)
```python
from graphene import Enum


class TaskStatus(Enum):
    BACKLOG = 0
    TODO = 1
    IN_PROGRESS = 2
    REVIEW = 3
    FINISH = 4
```

[object_types/task.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/object_types/task.py)
```python
import graphene
from enums import TaskStatus


class TaskFields(graphene.AbstractType):
    title = graphene.String()
    description = graphene.String()

class TaskObject(graphene.ObjectType, TaskFields):
    id = graphene.Int()
    status = graphene.Field(TaskStatus)
```

В [GraphQL](http://graphql.org/learn/) за обработку запросов отвечают два главных 
компонента 
[query](http://graphql.org/learn/queries/) 
и 
[mutation](http://graphql.org/learn/queries/#mutations). 
В данном случае нас интересуют 
[mutation](http://graphql.org/learn/queries/#mutations), которому в обязательном 
порядке надо создавать внутренний класс 
[Input](http://docs.graphene-python.org/en/latest/types/mutations/#inputfields-and-inputobjecttypes), атрибутами которого 
буду поля, которые мы можем передавать в нашу 
[mutation](http://docs.graphene-python.org/en/latest/types/mutations/).
Атрибут как и любой объект в GraphQL может быть любой вложенности, это может 
быть 
[graphene.InputObjectType](http://docs.graphene-python.org/en/latest/types/mutations/#inputfields-and-inputobjecttypes),
[Scalar](http://docs.graphene-python.org/en/latest/types/scalars/), 
или встроеный тип. 

Атрибуты класса мутации
являются, тем что мы можем вернуть в ответ на запрос, это может быть вновь 
созданный объект, 
[graphene.ObjectType](http://docs.graphene-python.org/en/latest/types/objecttypes/),
[Scalar](http://docs.graphene-python.org/en/latest/types/scalars/),
или встроеный тип. 

[mutations/inputs/task_input.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/mutations/inputs/task_input.py)
```python
class TaskInput(InputObjectType, TaskFields):
    pass
```

[mutations/create_task.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/mutations/create_task.py)
```python
class CreateTask(Mutation):

    class Input:
        task_data = Argument(TaskInput)

    task = Field(TaskObject)

    @staticmethod
    def mutate(root, args, context, info):
        store = context.get('store')
        task_data = args.get('task_data')
        task_data['status'] = TaskStatus.BACKLOG.value
        record = store.create_task(data=task_data)
        task = TaskObject(**record.as_dict)
        return CreateTask(task=task)
```

В результате мы можем выполнить [запрос](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/create_task/query.graphql)

![Create tasks](https://raw.githubusercontent.com/totaki/graphql-learn/develop/articles/ru/episode-2/create_task/createTask.gif)

Тут можете увидеть тип fragment в запросе позже, я объясню зачем это.

 