from graphene import Argument, Field, Int, Mutation
from object_types import TaskObject


class SetTaskParent(Mutation):

    class Input:
        parent_id = Argument(Int)
        child_id = Argument(Int)

    task = Field(lambda: TaskObject)

    @staticmethod
    def mutate(root, args, context, info):
        parent_id = args.get('parent_id')
        child_id = args.get('child_id')
        store = context.get('store')
        record = store.get(child_id)
        record.update(parent_id=parent_id)
        # TODO: надо парент тоже добавить в возвращаемый объект
        task_data = record.as_dict
        if 'iteration_id' in task_data.keys():
            task_data.pop('iteration_id')
        if 'parent_id' in task_data.keys():
            task_data.pop('parent')
        task = TaskObject(**task_data)
        return SetTaskParent(task=task)
