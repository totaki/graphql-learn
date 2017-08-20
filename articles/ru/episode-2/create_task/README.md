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
компонента [query](http://graphql.org/learn/queries/) и [mutation](http://graphql.org/learn/queries/#mutations).

 