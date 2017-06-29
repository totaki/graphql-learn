import json
from os import path


class JSONStore(object):

    def __init__(self, file_name='./data.json'):
        self.file_name = file_name
        self._next_index = 1
        self._current_data = {}

    def load(self):
        if path.isfile(self.file_name):
            with open(self.file_name) as f:
                self._current_data = json.load(f)
                self._next_index = len(self._current_data) + 1

    def dump(self):
        with open(self.file_name, 'w') as f:
            json.dump(self._current_data, f)

    def create(self, data):
        current_index = self._next_index
        self._current_data[str(current_index)] = data
        self._next_index += 1
        return current_index

    def update(self, key, data):
        self._current_data[str(key)] = data

    def get(self, key):
        data = self._current_data.get(str(key), None)
        if data:
            data['id'] = key
        return data

    def delete(self, key):
        del self._current_data[str(key)]