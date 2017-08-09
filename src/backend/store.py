class RecordAttributeError(Exception):

    def __init__(self, key, *args):
        message = (
            'Dictionary key must be not exist in object attributes: %s'
            % key
        )
        super().__init__(message, *args)


class Record(object):

    def __init__(self, index, kind, data=None):
        self.id = index
        self.kind = kind
        self._data = {}
        if data:
            self._check_data_attributes(data)
            self._data = data

    def _check_data_attributes(self, data):
        keys = set(data.keys()).intersection(dir(self))
        if len(keys):
            raise RecordAttributeError(keys)

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        else:
            return super().__getattribute__(name)

    def update(self, **kwargs):
        self._check_data_attributes(kwargs)
        self._data.update(**kwargs)

    @property
    def as_dict(self):
        dct = {'id': self.id}
        dct.update(self._data)
        return dct


class Store(object):
    def __init__(self):
        self._store = {}

    # TODO: maybe move data to **kwargs
    def create(self, kind, data):
        index = len(self._store.keys()) + 1
        record = Record(index, kind, data)
        self._store[index] = record
        return record

    def get(self, index):
        index = int(index)
        return self._store[index]

    def delete(self, index):
        index = int(index)
        del self._store[index]

    def all_by_kind(self, kind):
        return filter(lambda r: r.kind == kind, self._store.values())

    def all(self):
        return self._store.values()