"""This package use for create map from tarantool db to Python object,
and reverse.

>>> class TestMapper(BaseMapper):
...     fields = ('key1', 'key2')
...
>>> test_object = TestMapper(1, 'string value')
>>> test_object._fields_map
{'key1': 0, 'key2': 1}
>>> test_object.key1
1
>>> test_object.key2
'string value'
>>> test_object.key2 = 'new string'
>>> test_object.key2
'new string'
>>> test_object.as_dict()
{'key1': 1, 'key2': 'new string'}
>>> TestMapper(1, 'string value', 1)
Traceback (most recent call last):
    ...
AssertionError
"""


class MetaMapper(type):
    """Metaclass for all mappers. It's make field class attribute to
    _fields_map attribute as dict for all class based on this class, where key
    is name and value is position in initializate object args
    """

    def __new__(mcs, name, bases, attributes):
        attributes.update({'_fields_map': dict(
            [(i[1], i[0]) for i in enumerate(attributes['fields'])]
        )})
        return super().__new__(mcs, name, bases, attributes)


class BaseMapper(object, metaclass=MetaMapper):
    """Base class for all mappers make possible get and set attribute from
    _store by name
    """
    fields = ()

    def __init__(self, *args):
        assert len(args) == len(self.fields)
        self._store = list(args)

    def __getattr__(self, name):
        if name in self._fields_map:
            return self._store[self._fields_map[name]]
        else:
            return self.__dict__[name]

    def __setattr__(self, name, value):
        if name in self._fields_map:
            self._store[self._fields_map[name]] = value
        else:
            self.__dict__[name] = value

    def as_dict(self):
        """Translate fields and _store elements to dictonary
        Returns:
            dict: where keys and indexes get from _fields_map, value get from
            _store by indexes
        """
        return dict(
            [(k, self._store[v]) for k, v in self._fields_map.items()])
