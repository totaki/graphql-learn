[Назад](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/README.md#tree-tasks)|
-----|

В данном случае мы не будем строить длинные цепочки бизнес-логики, а я покажу,
как для нашых задач задавать родителя и получать его потомков, в котором будет также 
текущий объект, я думаю это объяснить идеи указанные в заголовке это части.
Задам нашим задачи еще два поля, это **parent** и **childs**. Надо обернуть их
в ```lambda: Type```, что бы могли сделать поле сылающееся само на себя. 

[object_types/task.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/object_types/task.py)
```python
class TaskObject(graphene.ObjectType, TaskFields):
    id = graphene.Int()
    status = graphene.Field(TaskStatus)
    parent = graphene.Field(lambda: TaskObject)
    childs = graphene.List(lambda: TaskObject)

    def resolve_parent(self, args, context, info):
        store = context.get('store')
        record = store.get(self.id)
        if record and record.parent_id:
            parent_record = store.get(record.parent_id)
            return TaskObject(**parent_record.as_dict)

    def resolve_childs(self, args, context, info):
        tasks = context['store'].all_by_kind('task')
        result = [
            TaskObject(**task.as_dict)
            for task in filter(lambda t: t.parent_id == self.id, tasks)
        ]
        return result
```

А также сделаем mutation для задания родителя нашей задаче.
[mutations/set_parent](https://github.com/totaki/graphql-learn/blob/develop/src/backend/mutations/set_parent)
```python
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
        task_data = record.as_dict
        task = TaskObject(**task_data)
        return SetTaskParent(task=task)
```

В результате мы можем выполнить [запрос](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/tree_tasks/query.graphql)
Как тут видно, мы можем бесконечно провалиться в наши поля **parent** и **childs**.
Т.е. если есть какая то связь по одному из полей с другой частью нашего приложения
мы можем его получить, это на мой взгляд одна из самых крутых фитч.

![Set parent task](https://raw.githubusercontent.com/totaki/graphql-learn/develop/articles/ru/episode-2/tree_tasks/setParentTask.gif)

