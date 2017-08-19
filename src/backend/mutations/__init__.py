from graphene import ObjectType
from .create_task import CreateTask
from .move_task import MoveTask
from .set_parent import SetTaskParent


class Mutations(ObjectType):
    create_task = CreateTask.Field()
    move_task = MoveTask.Field()
    set_parent = SetTaskParent.Field()