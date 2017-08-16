import graphene
from enums import TaskStatus


class TaskFields(graphene.AbstractType):
    title = graphene.String()
    description = graphene.String()


class TaskObject(graphene.ObjectType, TaskFields):
    id = graphene.Int()
    status = graphene.Field(TaskStatus)

