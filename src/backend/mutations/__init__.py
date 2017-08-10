from graphene import ObjectType
from .create_task import CreateTask
from .move_task import MoveTask


class Mutations(ObjectType):
    create_task = CreateTask.Field()
    move_task = MoveTask.Field()