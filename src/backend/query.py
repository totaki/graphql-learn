import graphene
import object_types
from utils import get_iteration_datetime


backlog_description = '''
This field include all tasks without iterationId
'''


class Query(graphene.ObjectType):
    backlog = graphene.List(object_types.TaskObject, description=backlog_description)
    dashboard = graphene.Field(object_types.IterationObject, iteration_id=graphene.Int(), offset=graphene.Int())

    def resolve_backlog(self, args, context, info):
        store = context.get('store')
        records = store.all_by_kind('task')
        tasks = [
            object_types.TaskObject(**record.as_dict)
            for record
            in filter(
                lambda r: not r.as_dict.get('iteration_id', None), records)
        ]
        return tasks

    def resolve_dashboard(self, args, context, info):
        iteration_dt = get_iteration_datetime(args)
        iterations = context['store'].all_by_kind('iteration')
        filtered_iterations = list(filter(lambda i: i.as_dict['start_date'] == iteration_dt, iterations))
        if filtered_iterations:
            return object_types.IterationObject(**filtered_iterations[0].as_dict)
        else:
            return object_types.IterationObject(id=None, start_date=iteration_dt)