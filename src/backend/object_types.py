import graphene
import abstracts


class TaskObject(graphene.ObjectType, abstracts.TaskFields):
    pass


class IterationObject(graphene.ObjectType, abstracts.IterationFields):
    tasks = graphene.List(TaskObject)

    def resolve_tasks(self, args, context, info):
        pass
