![Image of this Article](https://raw.githubusercontent.com/totaki/graphql-learn/develop/articles/main.png)

Список эпизодов:
* [Эпизод 1](https://github.com/totaki/graphql-learn/tree/develop/articles/ru/episode-1/README.md)
* Эпизод 2

# GraphQL и Python. Эпизод 2

## Наше приложение
Во многих примерах вы можете найти приложения типа TODO, со списком задач и полем ввода. Как мне кажется оно не отображает
всего того что есть в **GraphQL**, поэтому я решил в качестве примера взять расширенный TODO. Если быть точнее это будет 
какое-то подобие scrum/agile доски, включающее users, tasks, backlog, iteration, relation tasks и workflow.

Для начала небольшое ТЗ:
1. Backlog. Это список задач, которые не вошли ни в одну итерацию. Из него можно удалить задачу, а также перенести в итерацию
текущего контекста.
2. Iteration. Включает в себя список задач в этой итерации, а также дату начала и окончания. Каждая итерация имеет длительность
равной одной недели. Для того чтобы перенести задачу из одной итерации в другую, сначала надо вернуть ее бэклог, и переключить
контекст.
3. Task. Задача имеет название, описание, итерацию, состояние, ответсвенного пользователя и задачу родителя. Может быть
в трех состояниях **todo**, **in_progress**, **review**, **finish**. Задачи могут двигатся вперед и назад.
4. User. Имеет только имя и список задач, которые ему назначенны.

В этом эпизоде мы не будем делать клиентскую часть, а воспользуемся специальной **IDE** для **GraphQL**.

## Что нам для этого понадобится
1. [Python 3.6](https://www.python.org/downloads/)
2. [Tornado](http://www.tornadoweb.org/en/stable/)
3. [Graphene](http://graphene-python.org/)
4. [Docker](https://www.docker.com/) вместе с [docker-compose](https://docs.docker.com/compose/)
5. [GraphiQL](https://github.com/graphql/graphiql)
6. [Nginx](https://nginx.ru/ru/)

Сам deploy у нас будет незамысловатой.

![Image of this Article](https://raw.githubusercontent.com/totaki/graphql-learn/develop/articles/deploy_full_width.png)


## Cхема
Для того чтобы понять какие сущности нам нужны, нарисуем схему.

![Image of this Article](https://raw.githubusercontent.com/totaki/graphql-learn/develop/articles/sheme.png)


## Ну вот мы и добравлись до кода
#### Создаем хранилище
Первым делом мы создадим хранилище для наших данных, сделаем просто in-memory хранилище, в котором мы сможем наши записи
получать по ```id int```. Приложу [ссылку](https://github.com/totaki/graphql-learn/blob/develop/src/backend/store.py),
если кому интересно, к статье это не относится.

#### Создаем наше web-приложение
Мы возьмем tornado с одним единственным обработчиком ([приложение](https://github.com/totaki/graphql-learn/blob/develop/src/backend/main.py)), в само приложение мы передадим ```schema```, пока возьмем
с сайта пример, чтобы проверить просто работоспособность. 
```python
import graphene

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, args, context, info):
        return 'World'

schema = graphene.Schema(query=Query)
```

#### Создаем абстрактные классы
Следующим делом мы создадим наши абстаркные классы, унаследованные от 
[graphene.AbstractType](http://docs.graphene-python.org/en/latest/types/abstracttypes/). Они нужны нам для того
чтобы мы могли одни и теже поля получать и передавать как в [graphene.ObjectType](http://docs.graphene-python.org/en/latest/types/objecttypes/)
так и в [graphene.InputObjectType](http://docs.graphene-python.org/en/latest/types/mutations/)

[Код с комментариями и результат](https://github.com/totaki/graphql-learn/tree/develop/articles/ru/episode-2/code-1.md)


#### Создаем задачи
Теперь создадим наш первый ```ObjectType``` ```TaskObject```, для него создадим ```mutation``` для создания, а также запрос
на получение списка задач.

[Код с комментариями и результат](https://github.com/totaki/graphql-learn/tree/develop/articles/ru/episode-2/code-2.md)

#### Подвинем задачу в новую итерацию
Логика такая мы передаем в мутацию id нашей задачи, id итерации из контекста и текущую дату. Мы ищем итерцаю сначала по id
, потом по дате если не находим, тогда создаем новую. Если находим добавляем в список итераций. 


#### Итерации
Логика будет такая, мы изначально получаем наш текущую итерацию, если итерация с такой датой есть значит мы её отдаем, если 
нет отдаем итерацию с пустым списком задач. Итерация считается созданной когда мы в нее добавили хотябы одну задачу.

Новые этапы.
1. Первым делом надо показать как прикрутить graphql в handler и задать схему и передать контекст наш сторе (надо
упомянуть про проблемы которые были с ide).
2. Дальше мы должны добавить показать как нам добавить один таск, т.е. создание тасинфо, таск инпут и мутацию. Объяснить зачем нам абстрацкии
3. Дальше мы должны создать бэклог резолвео для получения наших тастков.
4. Мы должны создать дашбоард резолвер, для это надо добавить объект итерация со своей логикой, переключения между итерациями.
5. Мы должны сделать возможность переводить наши таски по статусам вперед назад при это при движении из бэклога если итерации нет
то она создается.
6. Мы должны на учится задавать родительский таск.
7. Мы должны научиться добавлять юзеров.
8. Сделать отсылку ошибок валидации


### Место жизни нашего приложения
Для обработки входящих запросов мы будем использовать **tornado**, у которого будет один единственный обработчик. Тут есть пара моментов
не указанных в документации. Когда я писал через тесты то передавал просто **query** в теле запроса, как строку (пример ```query { hello }```),
в последтвии когда подключил **GraphiQL**, увидел что там прилетает ```application/json``` и он в себя уже включает несколько полей, это **query** (сам запрос),
**variables** (опционально, переменные запроса, это объект) и **operationName** (опционально, название запроса, ```query helloQuery { hello }```). Мы получаем эти поля и передаем в наш
executor.

**main.GraphQLHandler.query_data**
```python
body = self.request.body.decode('utf-8')
content_type = self.request.headers.get_list('Content-Type')[0]
if 'application/json' in content_type:
    data = json.loads(body)
    query = data['query']
    variables = data.get('variables', None)
    operation_name = data.get('operationName', None)
```

**main.GraphQLHandler.get_response**
```python 
result = self.schema.execute(
    query,
    variable_values=variables,
    context_value={'store': self.store},
    operation_name=operation_name
)
```

### Создание задач
Попробуем создать наши первые задачи. Сначала мы создадим класс **TaskFields** от **graphene.AbstractType**. **AbstractType** это фишка самого graphene, 
он нам позволяет не писать каждый одни и теже поля для классов одной сущности. Например в данном случае у нас есть **TaskFields**:

**enums.task_status**
```python
class TaskStatus(Enum):
    BACKLOG = 0
    TODO = 1
    IN_PROGRESS = 2
    REVIEW = 3
    FINISH = 4
```

**mutations.inputs.task_input**
```python
class TaskInput(InputObjectType, TaskFields):
    pass
```
Данные поля нам понадобятся для самого **ObjectType** (сам объект запроса)и **InputObjectType** (данный класс нужен чтобы указать какие поля мы можем получить в нашей мутации)

**object_types.task**
```python
class TaskFields(graphene.AbstractType):
    title = graphene.String()
    description = graphene.String()

class TaskObject(graphene.ObjectType, TaskFields):
    id = graphene.Int()
    status = graphene.Field(TaskStatus)
```

**mutations.create_task**
```python
class CreateTask(Mutation):

    class Input:
        task_data = Argument(TaskInput)

    task = Field(TaskObject)

    @staticmethod
    def mutate(root, args, context, info):
        store = context.get('store')
        task_data = args.get('task_data')
        task_data['status'] = TaskStatus.BACKLOG.value
        record = store.create_task(data=task_data)
        task = TaskObject(**record.as_dict)
        return CreateTask(task=task)
```

**mutations.__init__**
```python
class Mutations(ObjectType):
    create_task = CreateTask.Field()
```

Теперь мы можем выполнять запросы на создание нашей задачи

```graphql
mutation createTask($title: String, $description: String) {
  createTask(taskData: {title: $title, description: $description}) {
    task {
      ... taskData
    }
  }
}

fragment taskData on TaskObject {
  id
  status
}
```
Variables
```json
{
  "title": "Task title",
  "description": "Task description"
}
```
В ответ получим
```json
{
  "errors": null,
  "data": {
    "createTask": {
      "task": {
        "id": 1,
        "status": "BACKLOG"
      }
    }
  }
}
```

### Получение backlog
Тут все просто мы создаем резолвер **resolve_backlog** который возвращает из БД объекты, у которых
нет атрибута iteration_id или он равен None. Мы также указываем, что у нас это список
объектов.

**query**
```python
class Query(graphene.ObjectType):

    backlog_description = '''
    This field include all tasks without iteration
    '''
    backlog = graphene.List(
        TaskObject, description=backlog_description
    )

    def resolve_backlog(self, args, context, info):
        tasks = context['store'].tasks
        return [
            TaskObject(**task.as_dict)
            for task in filter(lambda t: not t.iteration_id, tasks)
        ]
```

Запрос будет выглядить 
```graphql
query getBacklog {
  backlog {
    ... taskData
  }
}
```

В ответ мы получим 
```json
{
  "errors": null,
  "data": {
    "backlog": [
      {
        "id": 1,
        "status": "BACKLOG"
      },
      {
        "id": 2,
        "status": "BACKLOG"
      }
    ]
  }
}
```

### Работа с итерациями
В объекте итерации мы не будем хранить дату окончания итерации, а вычислять ее на лету, если нам надо это поле. Также мы не храним
наш объект пока в нем нет ни одной итерции.

**object_types.iteration**
```python
class IterationObject(graphene.ObjectType):
    id = graphene.Int()
    start_date = DateTime()
    tasks = graphene.List(TaskObject)
    end_date = DateTime()

    def resolve_tasks(self, args, context, info):
        result = []
        if self.id:
            tasks = context['store'].all_by_kind('task')
            result.extend([
                TaskObject(**task.as_dict)
                for task
                in filter(lambda t: t.as_dict.get('iteration_id', None) == self.id, tasks)
            ])
        return result

    def resolve_end_date(self, args, context, info):
        return self.start_date + dt.timedelta(days=6)
```

**query**
```python
class Query(graphene.ObjectType):

    ...

    dashboard = graphene.Field(
        IterationObject,
        iteration_id=graphene.Int(),
        offset=graphene.Int()
    )


    def resolve_dashboard(self, args, context, info):
        iteration_dt = get_iteration_datetime(args)
        iterations = context['store'].iterations
        filtered_iterations = list(filter(lambda i: i.start_date == iteration_dt, iterations))
        if filtered_iterations:
            return IterationObject(**filtered_iterations[0].as_dict)
        else:
            return IterationObject(id=None, start_date=iteration_dt)
```

**utils**
```python
def get_datetime(datetime=None, offset=0):
    if not datetime:
        datetime = dt.datetime.utcnow()
    delta = calendar.weekday(datetime.year, datetime.month, datetime.day)
    _ = datetime - dt.timedelta(days=delta) + dt.timedelta(days=offset * 7)
    return dt.datetime(_.year, _.month, _.day)


def get_iteration_datetime(args):
    return get_datetime(
        datetime=args.get('date', None),
        offset=args.get('offset', None)
    )
```

Пример запроса
```graphql
query getDashboard ($offset: Int){
  dashboard (offset: $offset){
    id
    startDate
    endDate
    tasks {
      ... taskData
    }
  }
}
```
Variables, переменная offset на сколько недель мы сместились от текущей даты итерации, дата итерации это первый день недели
```json
{
  "offset": 0
}
```
Ответ
```json
{
  "errors": null,
  "data": {
    "dashboard": {
      "id": null,
      "startDate": "2017-08-14T00:00:00",
      "endDate": "2017-08-20T00:00:00",
      "tasks": []
    }
  }
}
```

### Переводим наши таски
Давай научимся двигать наши таски из backlog в dashboard и по dashboard. Т.к. объект TaskObject у нас не содержит поля
iteration_id, мы будем удалять его из наших объектов.

**enums.task_status**
```python
class MovePositionTask(Enum):

    BACK = -1
    FORWARD = 1
```

**mutations.move_task**
```python
class MoveTask(Mutation):

    class Input:
        task_id = Argument(Int)
        position = Argument(MovePositionTask)
        iteration_id = Argument(Int)
        iteration_date = DateTime()

    task = Field(lambda: TaskObject)

    @staticmethod
    def mutate(root, args, context, info):
        store = context.get('store')
        id, position, iteration, date = get_args_by_list(
            args,
            ['task_id', 'position', 'iteration_id', 'iteration_date']
        )
        record = store.get(id)
        previous_status = record.status
        record.update(status=record.status + position)

        from_backlog, to_backlog = get_directions(next=record.status, prev=previous_status)
        if from_backlog:
            if iteration:
                record.update(iteration_id=iteration)
            else:
                date = get_datetime(date)
                iteration = store.create_iteration(start_date=date).id
                record.update(iteration_id=iteration)
        elif to_backlog:
            record.update(iteration_id=None)

        task_data = record.as_dict
        if 'iteration_id' in task_data.keys():
            task_data.pop('iteration_id')
        task = TaskObject(**task_data)
        return MoveTask(task=task)
```

**mutations.__init__**
```python
class Mutations(ObjectType):
    create_task = CreateTask.Field()
    move_task = MoveTask.Field()
```

Теперь подвигаем наши задачи вперед

```graphql
mutation moveTaskForward($taskId: Int) {
  moveTask(taskId: $taskId, position: FORWARD) {
    task {
      ... taskData
    }
  }
}
```
Variables
```json
{
  "taskId": 1
}
```

Ответ
```json
{
  "errors": null,
  "data": {
    "moveTask": {
      "task": {
        "id": 1,
        "status": "TODO"
      }
    }
  }
}
```

### Древовидная структура тасков
Добавим нашем задач родительскую задачу и задачи потомки. Если мы хотим указать что не которые поля являются теми же
объектами что и сам объект мы должны просто указать ```lambda: T```

**object_types.task**
```python
class TaskFields(graphene.AbstractType):
    title = graphene.String()
    description = graphene.String()

class TaskObject(graphene.ObjectType, TaskFields):
    id = graphene.Int()
    status = graphene.Field(TaskStatus)
    parent = graphene.Field(lambda: TaskObject)
```

