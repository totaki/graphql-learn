import graphene


class Record(object):
    def __init__(self, index, kind, data=None):
        self._id = index
        self._kind = kind
        self._data = data if data else {}

    def update(self, data):
        self._data.update(data)

    @property
    def as_dict(self):
        dct = {'id': self._id}
        dct.update(self._data)
        return dct


class Store(object):
    def __init__(self):
        self._store = {}

    def create(self, kind, data):
        index = len(self._store.keys())
        self._store[index] = Record(index, kind, data)

    def get(self, index):
        index = int(index)
        return self._store[index]

    def delete(self, index):
        index = int(index)
        del self._store[index]

    def all(self):
        return self._store.values()


app_data = {
    1: Record(1, 'user', {
        'username': 'user_name',
        'tasks': [2, 3, 4, 5]
    }),
    2: Record(2, 'task', {
        'title': 'Task title 1',
        'description': 'Taske description 1',
        'iteration': 6,
        'user': 1,
        'status': 0
    }),
    3: Record(3, 'task', {
        'title': 'Task title 2',
        'description': 'Taske description 2',
        'iteration': 6,
        'user': 1,
        'status': 0
    }),
    4: Record(4, 'task', {
        'title': 'Task title 3',
        'description': 'Taske description 3',
        'iteration': 6,
        'user': 1,
        'status': 0
    }),
    5: Record(5, 'task', {
        'title': 'Task title 4',
        'description': 'Taske description 4',
        'iteration': 6,
        'user': 1,
        'status': 0
    }),
    6: Record(6, 'iteration', {
        'start_date': '01-01-2017',
        'days': 7,
    }),
}

store = Store()
store._store = app_data


class StatusTask(graphene.Enum):
    TODO = 0
    IN_PROGRESS = 1
    REVIEW = 2
    FINISH = 3


class UserInfo(graphene.ObjectType):

    id = graphene.Int()
    username = graphene.String()


class TaskInfo(graphene.ObjectType):

    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    status = graphene.Field(StatusTask)


class IterationInfo(graphene.ObjectType):

    id = graphene.Int()
    start_date = graphene.String()
    days = graphene.Int()


class User(graphene.ObjectType):

    id = graphene.Int()
    info = graphene.Field(UserInfo)
    tasks = graphene.List(TaskInfo)


class Iteration(graphene.ObjectType):

    id = graphene.Int()
    info = graphene.Field(IterationInfo)
    tasks = graphene.List(TaskInfo)

    @staticmethod
    def _record_dict_to_task_instance(data):
        return TaskInfo(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            status=StatusTask(data['status'])
        )

    def resolve_tasks(self, args, context, info):
        tasks_records = filter(
            lambda r: r._kind == 'task' and r._data['iteration'] == self.id,
            store.all()
        )
        return [
            self._record_dict_to_task_instance(r.as_dict)
            for r in tasks_records
        ]


class Task(graphene.ObjectType):

    id = graphene.Int()
    info = graphene.Field(TaskInfo)
    iteration = graphene.Field(IterationInfo)
    user = graphene.Field(UserInfo)


class Query(graphene.ObjectType):

    dashboard = graphene.Field(Iteration)

    def resolve_dashboard(self, args, context, info):
        record_dict = store.get(6).as_dict
        iteration_info = IterationInfo(id=record_dict['id'], start_date=record_dict['start_date'], days=record_dict['days'])
        iteration = Iteration(id=6, info=iteration_info)
        return iteration


schema = graphene.Schema(query=Query)

if __name__ == '__main__':
    import pprint
    result = schema.execute('query {dashboard { id, tasks { id, title, description, user }}}')
    if result.errors:
        pprint.pprint(result.errors)
    else:
        pprint.pprint(result.data)