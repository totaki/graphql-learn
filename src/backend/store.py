class Record(object):
    def __init__(self, index, kind, data=None):
        self._id = index
        self._kind = kind
        self._data = data if data else {}

    def update(self, data):
        self._data.update(data)

    @property
    def as_dict(self):
        dct = {'id': self._id}
        dct.update(self._data)
        return dct


class Store(object):
    def __init__(self):
        self._store = {}

    def create(self, kind, data):
        index = len(self._store.keys())
        self._store[index] = Record(index, kind, data)

    def get(self, index):
        index = int(index)
        return self._store[index]

    def delete(self, index):
        index = int(index)
        del self._store[index]

    def all(self):
        return self._store.values()