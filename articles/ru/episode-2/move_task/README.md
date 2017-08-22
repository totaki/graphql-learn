[Назад](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/README.md#move-task)|
-----|

[enums/task_move_position.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/enums/task_move_position.py)
```python
class MovePositionTask(Enum):

    BACK = -1
    FORWARD = 1
```

[mutations/move_task.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/mutations/move_task.py)
```python
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

        from_backlog, to_backlog = get_directions(next=record.status, prev=previous_status)
        if from_backlog:
            if iteration:
                record.update(iteration_id=iteration)
            else:
                date = get_datetime(date)
                iteration = store.create_iteration(start_date=date).id
                record.update(iteration_id=iteration)
        elif to_backlog:
            record.update(iteration_id=None)

        task_data = record.as_dict
        if 'iteration_id' in task_data.keys():
            task_data.pop('iteration_id')
        task = TaskObject(**task_data)
        return MoveTask(task=task)
```

[mutations/__init__.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/mutations/__init__.py)
```python
class Mutations(ObjectType):
    create_task = CreateTask.Field()
    move_task = MoveTask.Field()
```

В результате мы можем выполнить [запрос](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/move_task/query.graphql)

![Move task(https://raw.githubusercontent.com/totaki/graphql-learn/develop/articles/ru/episode-2/move_task/moveTask.gif)