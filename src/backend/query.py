import datetime as dt
import calendar
import graphene
import object_types
from graphene.types.datetime import DateTime


backlog_description = '''
This field include all tasks without iterationId
'''


def get_first_iteration_day(datetime, offset):
     delta = calendar.weekday(datetime.year, datetime.month, datetime.day)
     _ = datetime - dt.timedelta(days=delta) + dt.timedelta(days=offset * 7)

     return dt.datetime(_.year, _.month, _.day)


class Query(graphene.ObjectType):
    backlog = graphene.List(object_types.TaskObject, description=backlog_description)
    dashboard = graphene.Field(object_types.IterationObject, iteration_id=graphene.Int(), offset=graphene.Int())

    def resolve_backlog(self, args, context, info):
        store = context.get('store')
        records = store.all_by_kind('task')
        tasks = [object_types.TaskObject(**r.as_dict) for r in records]
        return tasks

    def resolve_dashboard(self, args, context, info):
        offset = args.get('offset', 0)
        iteration_dt = get_first_iteration_day(
            dt.datetime.utcnow(),
            offset
        )
        iterations = context['store'].all_by_kind('iteration')
        filtered_iterations = list(filter(lambda i: i.as_dict['start_date'] == iteration_dt, iterations))
        if filtered_iterations:
            return object_types.IterationObject(**filtered_iterations[0].as_dict)
        else:
            return object_types.IterationObject(id=None, start_date=iteration_dt)