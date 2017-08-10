from graphene import Enum


class TaskStatus(Enum):
    BACKLOG = 0
    TODO = 1
    IN_PROGRESS = 2
    REVIEW = 3
    FINISH = 4
