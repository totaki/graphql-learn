import graphene
import object_types

backlog_description = '''
This field include all tasks without iterationId
'''


class Query(graphene.ObjectType):
    backlog = graphene.List(object_types.TaskObject, description=backlog_description)

    def resolve_backlog(self, args, context, info):
        store = context.get('store')
        records = store.all_by_kind('task')
        tasks = [object_types.TaskObject(**r.as_dict) for r in records]
        return tasks