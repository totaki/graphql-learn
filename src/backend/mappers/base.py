"""
    This package use for create map from tarantool db to Python object,
    and reverse.
>>> class TestMapper(BaseMapper):
...     _map = ('key1', 'key2') 
...
>>> test_object = TestMapper(1,2,3)
>>> test_object._map_dict
True
"""


class MetaMapper(type):
    """
     This class ne
    """

    def __new__(mcs, name, bases, attributes):
        attributes.update(
            {'_map_dict': dict(map(
                lambda elem: (elem[1], elem[0]),
                enumerate(attributes['_map'])
            ))}
        )
        return type(name, bases, attributes)


class BaseMapper(object, metaclass=MetaMapper):
    """
     This class ne
    """
    _map = ()

    def __init__(self, *args):
        self._store = args

    def __getattr__(self, name):
        return self.__dict__[name]

    def to_dict(self):
        """
            Some docstring
        """
