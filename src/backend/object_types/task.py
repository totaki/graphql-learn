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
    iteration = graphene.Field('object_types.iteration.IterationObject')

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

    @property
    def iteration_class(self):
        return self._meta.fields['iteration'].type

    def resolve_iteration(self, args, context, info):
        store = context.get('store')
        record = store.get(self.id)
        if record.iteration_id:
            iteration_record = store.get(record.iteration_id)
            return self.iteration_class(**iteration_record.as_dict)
