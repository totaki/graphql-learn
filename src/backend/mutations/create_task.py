from graphene import  Mutation, Argument, Field
from enums import TaskStatus
from object_types import TaskObject
from mutations.inputs import TaskInput


class CreateTask(Mutation):

    class Input:
        task_data = Argument(TaskInput)

    task = Field(lambda: TaskObject)

    @staticmethod
    def mutate(root, args, context, info):
        store = context.get('store')
        task_data = args.get('task_data')
        task_data['status'] = TaskStatus.BACKLOG.value
        record = store.create('task', data=task_data)
        task = TaskObject(**record.as_dict)
        return CreateTask(task=task)
