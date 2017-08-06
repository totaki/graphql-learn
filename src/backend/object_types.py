import graphene
import abstracts


class TaskObject(graphene.ObjectType, abstracts.TaskFields):
    pass