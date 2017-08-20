import datetime as dt
import graphene
from graphene.types.datetime import DateTime
from . import TaskObject


class IterationObject(graphene.ObjectType):
    id = graphene.Int()
    start_date = DateTime()
    tasks = graphene.List(TaskObject)
    end_date = DateTime()

    def resolve_tasks(self, args, context, info):
        result = []
        if self.id:
            tasks = context['store'].tasks
            result.extend([
                TaskObject(**task.as_dict)
                for task
                in filter(lambda t: t.iteration_id == self.id, tasks)
            ])
        return result

    def resolve_end_date(self, args, context, info):
        return self.start_date + dt.timedelta(days=6)