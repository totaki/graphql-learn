import graphene
import abstracts
import object_types


class MovePositionTask(graphene.Enum):

    BACK = -1
    FORWARD = 1


class TaskInput(graphene.InputObjectType, abstracts.TaskFields):
    pass


class CreateTask(graphene.Mutation):

    class Input:
        data = graphene.Argument(TaskInput)

    task = graphene.Field(lambda: object_types.TaskObject)

    @staticmethod
    def mutate(root, args, context, info):
        store = context.get('store')
        data = args.get('data')
        data['status'] = abstracts.TaskStatus.BACKLOG.value
        record = store.create('task', data)
        task = object_types.TaskObject(**record.as_dict)
        return CreateTask(task=task)


class MoveTask(graphene.Mutation):

    class Input:
        task_id = graphene.Argument(graphene.Int)
        position = graphene.Argument(MovePositionTask)

    task = graphene.Field(lambda: object_types.TaskObject)

    @staticmethod
    def mutate(root, args, context, info):
        store = context.get('store')
        id = args.get('task_id')
        position = args.get('position')
        record = store.get(id)
        record.update(status=record.as_dict['status'] + position)
        task = object_types.TaskObject(**record.as_dict)
        return MoveTask(task=task)


class Mutations(graphene.ObjectType):
    create_task = CreateTask.Field()
    move_task = MoveTask.Field()