from graphene import Argument, Field, Int, Mutation
from graphene.types.datetime import DateTime
from enums import MovePositionTask, TaskStatus
from object_types import TaskObject
from utils import get_datetime


class MoveTask(Mutation):

    class Input:
        task_id = Argument(Int)
        position = Argument(MovePositionTask)
        iteration_id = Argument(Int)
        iteration_date = DateTime()

    task = Field(lambda: TaskObject)

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
            record.as_dict['status'] == TaskStatus.TODO
            and previous_status == TaskStatus.BACKLOG
        )
        if move_from_backlog:
            iteration_id = args.get('iteration_id', None)
            if iteration_id:
                record.update(iteration_id=iteration_id)
            else:
                date = get_datetime(args.get('iteration_date'))
                iteration = store.create('iteration', {'start_date': date})
        record.update(iteration_id=iteration.id)
        task = TaskObject(**record.as_dict)
        return MoveTask(task=task)
