from graphene import InputObjectType
from object_types import TaskFields


class TaskInput(InputObjectType, TaskFields):
    pass
