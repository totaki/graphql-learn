import datetime as dt
import graphene
import abstracts
from graphene.types.datetime import DateTime


class TaskObject(graphene.ObjectType, abstracts.TaskFields):
    pass


class IterationObject(graphene.ObjectType, abstracts.IterationFields):
    tasks = graphene.List(TaskObject)
    end_date = DateTime()

    def resolve_tasks(self, args, context, info):
        result = []
        if self.id:
            tasks = context['store'].all_by_kind('task')
            result.extend([
                TaskObject(**task.as_dict)
                for task
                in filter(lambda t: t.as_dict['iteration_id'] == self.id, tasks)
            ])
        return result

    def resolve_end_date(self, args, context, info):
        return self.start_date + dt.timedelta(days=6)