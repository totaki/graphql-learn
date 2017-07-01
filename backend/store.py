import json
from os import path


class DictStore(object):

    def __init__(self, data=None):
        self._store = data or {}
        self._next_index = len(self._store.keys()) + 1

    def create(self, data: dict) -> int:
        current_index = self._next_index
        self._store[str(current_index)] = data
        self._next_index += 1
        return current_index

    def update(self, key: int, data: dict) -> int:
        self._store[str(key)] = data
        return key

    def get(self, key: int) -> dict:
        data = self._store.get(str(key), None)
        if data:
            data['id'] = key
        return data

    def delete(self, key: int) -> None:
        del self._store[str(key)]

    def all(self):
        return self._store


class JSONStore(object):

    def __init__(self, stores: list, file_name='./data.json'):
        self.file_name: str = file_name
        self._stories_names = stores
        self._stories: dict = {s: DictStore() for s in stores}
        for k, v in self._stories.items():
            setattr(self, k, v)

    def load(self) -> None:
        if path.isfile(self.file_name):
            with open(self.file_name) as f:
                self._stories = json.load(f)
            for s in self._stories_names:
                setattr(self, s, DictStore(self._stories[s]))

    def dump(self, file_name: str=None) -> None:
        with open(file_name or self.file_name, 'w') as f:
            data_for_dump = {k: self._stories[k].all() for k in self._stories.keys()}
            json.dump(data_for_dump, f)
