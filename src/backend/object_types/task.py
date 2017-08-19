import graphene
from enums import TaskStatus


class TaskFields(graphene.AbstractType):
    title = graphene.String()
    description = graphene.String()


class TaskObject(graphene.ObjectType, TaskFields):
    id = graphene.Int()
    status = graphene.Field(TaskStatus)
    parent = graphene.Field(lambda: TaskObject)
    childs = graphene.List(lambda: TaskObject)

    # TODO: сделать нормыльный метод для создания таска
    def resolve_parent(self, args, context, info):
        store = context.get('store')
        record = store.get(self.id)
        task_data = record.as_dict
        if 'iteration_id' in task_data.keys():
            task_data.pop('iteration_id')
        if 'parent_id' in task_data.keys():
            task_data.pop('parent')
        return TaskObject(**task_data)

    def resolve_childs(self, args, context, info):
        pass
