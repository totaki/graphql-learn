from graphene import InputObjectType
from abstracts import TaskFields


class TaskInput(InputObjectType, TaskFields):
    pass
