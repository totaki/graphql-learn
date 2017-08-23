[Назад](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/README.md#circular_import)|
-----|

Как оказалось если мы передадим в ```graphene.Field``` строчку импорта нужного
нам класса, [Graphene](http://graphene-python.org/) все сам за нас сделает, а
нужный тип потом можно получить через ```self._meta.fields[field_name].type```.
Добам нашим задачам еще и итерации.

[object_types/task.py](https://github.com/totaki/graphql-learn/blob/develop/src/backend/object_types/task.py)
```python
class TaskObject(graphene.ObjectType, TaskFields):

    ...

    iteration = graphene.Field('object_types.iteration.IterationObject')

    ...
    
    @property
    def iteration_class(self):
        return self._meta.fields['iteration'].type

    def resolve_iteration(self, args, context, info):
        store = context.get('store')
        record = store.get(self.id)
        if record.iteration_id:
            iteration_record = store.get(record.iteration_id)
            return self.iteration_class(**iteration_record.as_dict)

```

В результате мы можем выполнить [запрос](https://github.com/totaki/graphql-learn/blob/develop/articles/ru/episode-2/circular_import/query.graphql)

![Circular import](https://raw.githubusercontent.com/totaki/graphql-learn/develop/articles/ru/episode-2/circular_import/circularImport.gif)
 