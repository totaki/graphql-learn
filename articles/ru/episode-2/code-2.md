![Image of this Article](https://raw.githubusercontent.com/totaki/graphql-learn/develop/articles/main.png)

[<<Назад](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/README.md#%D0%A1%D0%BE%D0%B7%D0%B4%D0%B0%D0%B5%D0%BC-%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B8)

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
Запросы к IDE. Тут я поясню, фрагменты позволяют нам не писать каждый, что мы хотим запросить, а сделать это один раз
![Create tasks](https://raw.githubusercontent.com/totaki/graphql-learn/develop/articles/gif/create_tasks.gif)

[<<Назад](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/README.md#%D0%A1%D0%BE%D0%B7%D0%B4%D0%B0%D0%B5%D0%BC-%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B8)
