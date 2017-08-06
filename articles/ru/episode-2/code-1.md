[<<Назад](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/README.md#%D0%A1%D0%BE%D0%B7%D0%B4%D0%B0%D0%B5%D0%BC-%D0%B0%D0%B1%D1%81%D1%82%D1%80%D0%B0%D0%BA%D1%82%D0%BD%D1%8B%D0%B5-%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D1%8B)

[develop/src/backend/abstracts.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/abstracts.py)
```python
import graphene
from graphene.types.datetime import DateTime


class TaskStatus(graphene.Enum):
    TODO = 1
    IN_PROGRESS = 2
    REVIEW = 3
    FINISH = 4


class UserFields(graphene.AbstractType):
    id = graphene.Int()
    name = graphene.String()
    tasks_id = graphene.List(graphene.Int)


class TaskFields(graphene.AbstractType):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    user_id = graphene.Int()
    iteration_id = graphene.Int()
    parent_id = graphene.Int()
    status = TaskStatus()


class IterationFields(graphene.AbstractType):
    id = graphene.Int()
    start_date = DateTime()
    end_date = DateTime()
    task_ids = graphene.List(graphene.Int)
```

[<<Назад](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/README.md#%D0%A1%D0%BE%D0%B7%D0%B4%D0%B0%D0%B5%D0%BC-%D0%B0%D0%B1%D1%81%D1%82%D1%80%D0%B0%D0%BA%D1%82%D0%BD%D1%8B%D0%B5-%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D1%8B)
