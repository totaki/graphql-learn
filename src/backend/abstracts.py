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
