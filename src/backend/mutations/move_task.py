from graphene import Argument, Field, Int, Mutation
from graphene.types.datetime import DateTime
from enums import MovePositionTask
from object_types import TaskObject
from utils import get_datetime, get_directions, get_args_by_list


class MoveTask(Mutation):

    class Input:
        task_id = Argument(Int)
        position = Argument(MovePositionTask)
        iteration_id = Argument(Int)
        iteration_date = DateTime()

    task = Field(lambda: TaskObject)

    @staticmethod
    def mutate(root, args, context, info):
        store = context.get('store')
        id, position, iteration, date = get_args_by_list(
            args,
            ['task_id', 'position', 'iteration_id', 'iteration_date']
        )
        record = store.get(id)
        previous_status = record.status
        record.update(status=record.status + position)

        from_backlog, to_backlog = get_directions(
            next=record.status, prev=previous_status
        )
        if from_backlog:
            if iteration:
                record.update(iteration_id=iteration)
            else:
                date = get_datetime(date)
                iteration = store.create_iteration(start_date=date).id
                record.update(iteration_id=iteration)
        elif to_backlog:
            record.update(iteration_id=None)

        task = TaskObject(**record.as_dict)
        return MoveTask(task=task)
