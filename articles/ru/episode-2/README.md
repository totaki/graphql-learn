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


## Ну вот мы и добрались до кода
#### Xранилище
Первым делом мы создадим хранилище для наших данных, сделаем просто in-memory хранилище, в котором мы сможем наши записи
получать по ```id int```. Приложу [ссылку](https://github.com/totaki/graphql-learn/blob/develop/src/backend/store/__init__.py),
если кому интересно, к статье это не относится.

----

#### Create application
Создаем наше web-приложение, тут и далее я не буду вставлять код, а на каждый пункт
создам отдельный файл с кодом, комментариями и примерами. В этом пункте
показано, как создать [RequestHandler](http://www.tornadoweb.org/en/stable/web.html#request-handlers)
и как правильно в нем получить данные [GraphQL запроса](http://graphql.org/learn/serving-over-http/)

[Перейти](https://github.com/totaki/graphql-learn/tree/develop/articles/ru/episode-2/application/README.md)

----

#### Create tasks
Создание задач. Здесь мы узнаем, как в [GraphQL](http://graphql.org/learn/) подошли
к изменению данных, а также узнаем некоторые вспомогательные моменты.

[Перейти](https://github.com/totaki/graphql-learn/tree/develop/articles/ru/episode-2/create_task/README.md)

----

#### Get backlog
Теперь настало время сделать наш первый resolver, этот метод как раз отвечает за получение данных конкретного поля.

[Перейти](https://github.com/totaki/graphql-learn/tree/develop/articles/ru/episode-2/backlog/README.md)

----

#### Get dashboard
Перейдем к следующему нашему resolver. Тут не будет новых концепций, я просто
хочу показать, как удобно сделаны вычисляемые поля.

[Перейти](https://github.com/totaki/graphql-learn/tree/develop/articles/ru/episode-2/dashboard/README.md)

----


Новые этапы.

4. Мы должны создать дашбоард резолвер, для это надо добавить объект итерация со своей логикой, переключения между итерациями.
5. Мы должны сделать возможность переводить наши таски по статусам вперед назад при это при движении из бэклога если итерации нет
то она создается.
6. Мы должны на учится задавать родительский таск.
7. Мы должны сделать что задачи также знали об итерации.
8. Сделать отсылку ошибок валидации (в grapqhl.error есть специальные ошибки)


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
    childs = graphene.List(lambda: TaskObject)

    def resolve_parent(self, args, context, info):
        store = context.get('store')
        record = store.get(self.id)
        if record and record.parent_id:
            parent_record = store.get(record.parent_id)
            return TaskObject(**parent_record.as_dict)

    def resolve_childs(self, args, context, info):
        tasks = context['store'].all_by_kind('task')
        result = [
            TaskObject(**task.as_dict)
            for task in filter(lambda t: t.parent_id == self.id, tasks)
        ]
        return result
```

**mutations.set_parent**
```python
class SetTaskParent(Mutation):

    class Input:
        parent_id = Argument(Int)
        child_id = Argument(Int)

    task = Field(lambda: TaskObject)

    @staticmethod
    def mutate(root, args, context, info):
        parent_id = args.get('parent_id')
        child_id = args.get('child_id')
        store = context.get('store')
        record = store.get(child_id)
        record.update(parent_id=parent_id)
        task_data = record.as_dict
        task = TaskObject(**task_data)
        return SetTaskParent(task=task)
```

Как создали таски писать не буду, сразу на то как им установить родителя

```graphql
mutation setParentTask($parentId: Int, $childId: Int) {
  setParent(parentId: $parentId, childId: $childId) {
    task {
      parent {
        id
        childs {
          id
        }
      }
    }
  }
}
```

Variables
```json
{
  "parentId": 1,
  "childId": 2
}
```

Пример отверта
```json
{
  "errors": null,
  "data": {
    "setParent": {
      "task": {
        "parent": {
          "id": 1,
          "childs": [
            {
              "id": 2
            }
          ]
        }
      }
    }
  }
}
```
Вообще по мне то что мы можемь так циклически резолвит типы сами на себя мега крутая
штука.


### Избавляемся от циклического импорта
Тут тоже создадетли graphql позаботились об этом. Если мы вместо типа передадим строку в наш field,
тогда он сам его заимпортирует, а в последствии мы сможем к нему обратиться через self._meta.fields[T].type