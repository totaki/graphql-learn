import os
import json
import pytest
from store import JSONStore
from schema import Schema
from main import make_app


@pytest.fixture
def store_test():
    store_name = 'test_store.json'
    store = JSONStore(['test'], store_name)
    store.load()
    yield store
    if os.path.isfile(store_name):
        os.remove(store_name)


@pytest.fixture
def store_app():
    store_name = 'test_store.json'
    store = JSONStore(['task', 'board'], store_name)
    store.load()
    yield store
    if os.path.isfile(store_name):
        os.remove(store_name)


@pytest.fixture
def schema(store_app):
    return Schema(store_app)


@pytest.fixture
def app():
    return make_app('config_test.yml')


@pytest.fixture
def get_response_field():
    def _(response, *args):
        data = json.loads(response.body.decode('utf-8'))
        for arg in args:
            data = data[arg]
        return data
    return _