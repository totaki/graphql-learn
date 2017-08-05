from store import JSONStore


def test_dump_store_and_get(store):
    data = {'key': 'value'}
    index = store.create(data)
    store.dump()
    loaded_store = JSONStore(store.file_name)
    loaded_store.load()
    data['id'] = index
    assert loaded_store.get(index) == data


def test_store_update_record(store):
    updated_data = {'updated_key': 'value', 'key': 'updated_value'}
    index = store.create({'key': 'value'})
    store.update(index, updated_data)
    assert store.get(index) == updated_data


def test_store_delete_record(store):
    index = store.create({})
    store.delete(index)
    assert not store.get(index)