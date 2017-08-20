from .record import Record


class InMemoryStore(object):
    def __init__(self):
        self._store = {}

    def create(self, kind, data=None, record_class=Record, **kwargs):
        index = len(self._store.keys()) + 1
        if data:
            record = record_class(index, kind, data)
        else:
            record = record_class(index, kind, kwargs)
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