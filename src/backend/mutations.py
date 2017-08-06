import graphene
import abstracts
import object_types


class TaskInput(graphene.InputObjectType, abstracts.TaskFields):
    pass


class CreateTask(graphene.Mutation):

    class Input:
        data = graphene.Argument(TaskInput)

    task = graphene.Field(lambda: object_types.TaskObject)

    @staticmethod
    def mutate(root, args, context, info):
        store = context.get('store')
        record = store.create('task', args.get('data'))
        task = object_types.TaskObject(**record.as_dict)
        return CreateTask(task=task)


class Mutations(graphene.ObjectType):
    create_task = CreateTask.Field()