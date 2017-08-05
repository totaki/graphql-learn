Первым делом нам надо где-то хранить наши данные. Для этого мы не будем прикручивать какую-то БД, а сделать просто класс хранилище и для класс для записей. Наш класс-хранилище сможет создавать, запрашивать по id, получать все записи и удалять записи. Класс записи сможет только обновлять свои данные


```python
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
        del self._data[index]
    
    def all(self)
        return self._data.values()
```

Теперь давайте сделаем какой-то наполненый сторе для нашего приложения
```python
app_data = {
    1: Record(1, 'user', {
        'name': 'user_name',
        'tasks': [2, 3, 4, 5]
    }),
    2: Record(2, 'task', {
        'title': 'Task title 1',
        'description': 'Taske description 1'
        'iteration': 6,
        'user': 1,
        'status': 0
    }),
    3: Record(3, 'task', {
        'title': 'Task title 2',
        'description': 'Taske description 2'
        'iteration': 6,
        'user': 1,
        'status': 0
    }),
    4: Record(4, 'task', {
        'title': 'Task title 3',
        'description': 'Taske description 3'
        'iteration': 6,
        'user': 1,
        'status': 0
    }),
    5: Record(5, 'task', {
        'title': 'Task title 4',
        'description': 'Taske description 4'
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
store._data = app_data
```

Т.к. у нас доска задач их необходиммо кому-то назначать, добавим в наше приложение класс User(graphene.ObjectType)

```python
class User(graphene.ObjectType):

    id = graphene.Int()
    name = graphene.String()
```

Мы делаем scrum-доску и нам нужны итерации
```python
class Iteration(graphene.ObjectType):

    id = graphene.Int()
    start_date = graphene.String()
    days = graphene.Int()
```

Наши задачи будут обладать стутусом
```python
class StatusTask(graphene.Enum):
    TODO = 0
    INPROGRESS = 1
    REVIEW = 2
    FINISH = 3
```

Самое главное нам нажну задачи
```python
class Task(graphene.ObjectType):

    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
```  

Теперь у нас есть все базовые модели, осталось их связать


Теперь мы должны выстроить наши связи:
1. У пользователя могут задачи
2. У итераций могут быть задачи
3. У задач может быть пользователь, итерация, статус и родитель.

```python
class User(graphene.ObjectType):

    id = graphene.Int()
    name = graphene.String()
    tasks = graphene.List(Task)
```

```python
class Iteration(graphene.ObjectType):

    id = graphene.Int()
    start_date = graphene.String()
    days = graphene.Int()
    tasks = graphene.List(Task)

    @staticmethod
    def _record_dict_to_task_instance(data):
        return Task(
            id=data['id'] ,
            title=data['title'],
            description=data['desription'],
            status=StatusTask(data['status'])
        )

    def resolve_tasks(self, args, context, info)
        tasks_records = filter(
            lambda: r: r.kind == 'task' and r.data['iteration'] == self.id,
            store.all()
        return [
            self._record_dict_to_task_instance(r.as_dict)
            for r in tasks_records
        ]
    )
```

```python
class Task(graphene.ObjectType):

    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    iteration = graphene.Field(Task)
    user = graphene.Field(User)
    status = graphene.Field(Status)

```  

Теперь создадим схему для типа dashboard, его идея в том что туда попадает итерация у которой время начала меньше текущего и время окончания больше текущего, но для простоты мы поку будем возвращать единственную итерацию которая у нас есть.

```python
class Query(graphene.ObjectType):
    
    dashboard = graphene.Field(Interation)

    def resolve_dashboard(self, args, context, info):
        record_dict = store.get(6).as_dict
        iteration = Iteration(id=record_dict['id'], start_data=record_dict['start_date'], days=record_dict['days'])
        return iteration
```