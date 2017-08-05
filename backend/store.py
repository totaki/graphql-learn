import json
from os import path


class JSONStore(object):

    def __init__(self, file_name: str='./data.json'):
        self.file_name = file_name
        self._next_index = 1
        self._store = {}

    def load(self) -> None:
        if path.isfile(self.file_name):
            with open(self.file_name) as f:
                self._store = json.load(f)
                self._next_index = len(self._store.keys())

    def dump(self, file_name: str=None) -> None:
        with open(file_name or self.file_name, 'w') as f:
            json.dump(self._store, f)

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
