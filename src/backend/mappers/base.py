"""
    This package use for create map from tarantool db to Python object,
    and reverse.
>>> class TestMapper(BaseMapper):
...     pass
...
>>> test_object = TestMapper(1,2,3)
>>> test_object._store
(1, 2, 3)
"""


class BaseMapper(object):
    """
        Some docstring
    """

    def __init__(self, *args):
        self._store = args

    def __getattr__(self, name):
        return self.__dict__[name]

    def to_dict(self):
        """
            Some docstring
        """
