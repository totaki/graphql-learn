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
Для обработки входящих запросов мы будем использовать tornado, у которого будет один единственный обработчик. Тут есть пара моментов
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
