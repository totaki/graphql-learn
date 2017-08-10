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
        tasks = context['store'].tasks
        return [
            object_types.TaskObject(**task.as_dict)
            for task in filter(lambda t: not t.iteration_id, tasks)
        ]

    def resolve_dashboard(self, args, context, info):
        iteration_dt = get_iteration_datetime(args)
        iterations = context['store'].iterations
        filtered_iterations = list(filter(lambda i: i.start_date == iteration_dt, iterations))
        if filtered_iterations:
            return object_types.IterationObject(**filtered_iterations[0].as_dict)
        else:
            return object_types.IterationObject(id=None, start_date=iteration_dt)