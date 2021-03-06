import graphene
from graphql import GraphQLError
from object_types import *
from utils import get_iteration_datetime


class Query(graphene.ObjectType):

    backlog_description = '''
    This field include all tasks without iteration
    '''
    backlog = graphene.List(
        TaskObject, description=backlog_description
    )

    dashboard = graphene.Field(
        IterationObject,
        iteration_id=graphene.Int(),
        offset=graphene.Int()
    )

    error = graphene.String()

    def resolve_backlog(self, args, context, info):
        tasks = context['store'].tasks
        return [
            TaskObject(**task.as_dict)
            for task in filter(lambda t: not t.iteration_id, tasks)
        ]

    def resolve_dashboard(self, args, context, info):
        iteration_dt = get_iteration_datetime(args)
        iterations = context['store'].iterations
        filtered_iterations = list(filter(lambda i: i.start_date == iteration_dt, iterations))
        if filtered_iterations:
            return IterationObject(**filtered_iterations[0].as_dict)
        else:
            return IterationObject(id=None, start_date=iteration_dt)

    def resolve_error(self, *args):
        return GraphQLError('Custom application error')