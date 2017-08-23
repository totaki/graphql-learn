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

#### Move task
Эта часть является вспомогательнной для нашего приложения. Тут показано, как вообще удобно прятать логику
работы приложения в resolver или mutations на примере изменения статуса задачи


[Перейти](https://github.com/totaki/graphql-learn/tree/develop/articles/ru/episode-2/move_task/README.md)

----

#### Tree tasks
Что мне нравится в [GraphQL](http://graphql.org), так это resolvers, они позволяет
нам из одного объекта получить доступ (если есть связь в промежуточных конечно)
к другому на противополжном конце бизнес-логики. Это я и продемонстрирую.

[Перейти](https://github.com/totaki/graphql-learn/tree/develop/articles/ru/episode-2/tree_tasks/README.md)

----



Новые этапы.

7. Мы должны сделать что задачи также знали об итерации.
8. Сделать отсылку ошибок валидации (в grapqhl.error есть специальные ошибки)

### Избавляемся от циклического импорта
Тут тоже создадетли graphql позаботились об этом. Если мы вместо типа передадим строку в наш field,
тогда он сам его заимпортирует, а в последствии мы сможем к нему обратиться через self._meta.fields[T].type