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
            for task in filter(lambda t: t.parent_id  == self.id, tasks)
        ]
        return result
