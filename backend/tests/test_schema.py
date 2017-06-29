def test_test_schema(schema):
    result = schema.execute('query { test }')
    assert not result.errors
    assert result.data['test']


def test_get_task(schema):
    data = {'title': 'Title test', 'description': 'Description test'}
    id = schema.store.create(data)
    result = schema.execute('query { task (id: 1) { title, description } }')
    assert result.data['task']['title'] == data['title']
    assert result.data['task']['description'] == data['description']