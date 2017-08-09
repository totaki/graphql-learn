import graphene
import abstracts
import object_types

from graphene.types.datetime import DateTime
from utils import get_datetime


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
        iteration_id = graphene.Argument(graphene.Int)
        iteration_date = DateTime()

    task = graphene.Field(lambda: object_types.TaskObject)

    @staticmethod
    def mutate(root, args, context, info):
        # TODO: create back to backlog logic
        store = context.get('store')
        id = args.get('task_id')
        position = args.get('position')
        record = store.get(id)
        previous_status = record.as_dict['status']
        record.update(status=record.as_dict['status'] + position)
        move_from_backlog = (
            record.as_dict['status'] == abstracts.TaskStatus.TODO
            and previous_status == abstracts.TaskStatus.BACKLOG
        )
        if move_from_backlog:
            iteration_id = args.get('iteration_id', None)
            if iteration_id:
                record.update(iteration_id=iteration_id)
            else:
                date = get_datetime(args.get('iteration_date'))
                iteration = store.create('iteration', {'start_date': date})
        record.update(iteration_id=iteration.id)
        task = object_types.TaskObject(**record.as_dict)
        return MoveTask(task=task)


class Mutations(graphene.ObjectType):
    create_task = CreateTask.Field()
    move_task = MoveTask.Field()