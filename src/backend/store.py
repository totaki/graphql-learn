class Record(object):
    def __init__(self, index, kind, data=None):
        self._id = index
        self.kind = kind
        self._data = data if data else {}

    def update(self, **kwargs):
        self._data.update(**kwargs)

    @property
    def as_dict(self):
        dct = {'id': self._id}
        dct.update(self._data)
        return dct


class Store(object):
    def __init__(self):
        self._store = {}

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