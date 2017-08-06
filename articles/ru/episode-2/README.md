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
1. Первым делом мы создадим хранилище для наших данных, сделаем просто in-memory хранилище, в котором мы сможем наши записи
получать по ```id int```. Приложу [ссылку](https://raw.githubusercontent.com/totaki/graphql-learn/develop/src/backend/store.py),
если кому интересно, к статье это не относится.
2. Следующим делом мы создадим наши абстаркные классы, унаследованные от 
[graphene.AbstractType](http://docs.graphene-python.org/en/latest/types/abstracttypes/). Они нужны нам для того
чтобы мы могли одни и теже поля получать и передавать как в [graphene.ObjectType](http://docs.graphene-python.org/en/latest/types/objecttypes/)
так и в [graphene.InputObjectType](http://docs.graphene-python.org/en/latest/types/mutations/)

[develop/src/backend/abstracts.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/abstracts.py)
```python
import graphene
from graphene.types.datetime import DateTime


class TaskStatus(graphene.Enum):
    TODO = 1
    IN_PROGRESS = 2
    REVIEW = 3
    FINISH = 4


class UserFields(graphene.AbstractType):
    id = graphene.Int()
    name = graphene.String()
    tasks_id = graphene.List(graphene.Int)


class TaskFields(graphene.AbstractType):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    user_id = graphene.Int()
    iteration_id = graphene.Int()
    parent_id = graphene.Int()
    status = TaskStatus()


class IterationFields(graphene.AbstractType):
    id = graphene.Int()
    start_date = DateTime()
    end_date = DateTime()
    task_ids = graphene.List(graphene.Int)
```
3. Теперь создадим наш первый ```ObjectType``` ```TaskObject```, для него создадим ```mutation``` для создания, а также запрос
на получение списка задач.

[develop/src/backend/object_types.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/object_types.py)
```python
import graphene
import object_types

# Наш новый объект задач, пока оставим его пустым, все поля которые есть
# будут отнаследованы от абстрактного класса
class TaskObject(graphene.ObjectType, abstracts.TaskFields):
    pass
```

[develop/src/backend/mutations.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/mutations.py)
```python
import graphene
import abstracts
import object_types


# То о чем писали выше, наш асбтрактный класс задал поля, как для входных, так и выходных данных
class TaskInput(graphene.InputObjectType, abstracts.TaskFields):
    pass


# У мутации мы должны указывать какие поля хотим получить, и что хотим возвратить
class CreateTask(graphene.Mutation):

    class Input:
        data = graphene.Argument(TaskInput)

    # Тут может быть что угодно, число, строка
    task = graphene.Field(lambda: object_types.TaskObject)

    @staticmethod
    def mutate(root, args, context, info):
        store = context.get('store')
        record = store.create('task', args.get('data'))
        task = object_types.TaskObject(**record.as_dict)
        return CreateTask(task=task)


# В GraphQL есть два больших объекта query и mutation, поэтому мы всегда должны их собирать из более мелких
class Mutations(graphene.ObjectType):
    create_task = CreateTask.Field()
```
Запросы для IDE
```javascript
mutation createTask($title: String, $description: String){
 	createTask(data: {title: $title, description: $description}) {
   	task {
      ...taskFields
    }
 	}
}

# Тут я поясню, фрагменты позволяют нам не писать каждый, что мы хотим запросить, а сделать это один раз
fragment taskFields on TaskObject {
	id,
  title,
  iterationId
}
```
Переменные запроса
```json
{
  "title": "Task title",
  "description": "Task description"
}
```
Результат запроса
```json
{
  "errors": null,
  "data": {
    "createTask": {
      "task": {
        "id": 2,
        "title": "Task title",
        "iterationId": null
      }
    }
  }
}
```
