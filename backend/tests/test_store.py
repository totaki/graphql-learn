from store import JSONStore


def test_dump_store_and_get(store_test):
    data = {'key': 'value'}
    index = store_test.test.create(data)
    store_test.dump()
    loaded_store = JSONStore(['test'], store_test.file_name)
    loaded_store.load()
    data['id'] = index
    assert loaded_store.test.get(index) == data


def test_store_update_record(store_test):
    updated_data = {'updated_key': 'value', 'key': 'updated_value'}
    index = store_test.test.create({'key': 'value'})
    store_test.test.update(index, updated_data)
    assert store_test.test.get(index) == updated_data


def test_store_delete_record(store_test):
    index = store_test.test.create({})
    store_test.test.delete(index)
    assert not store_test.test.get(index)