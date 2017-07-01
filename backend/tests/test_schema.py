def test_test_schema(schema):
    result = schema.execute('query { test }')
    assert not result.errors
    assert result.data['test']


def test_get_task(schema):
    data = {'title': 'Title test', 'description': 'Description test', 'status': 0}
    id = schema.store.task.create(data)
    result = schema.execute(f'''query {{ 
        task (id: {id}) {{
            title, description, status
        }} 
    }}''')
    assert result.errors is None
    assert result.data['task']['title'] == data['title']
    assert result.data['task']['description'] == data['description']


def test_create_task(schema):
    title = 'Title test'
    description = 'Create new task'
    result = schema.execute(f'''mutation {{
        createTask (data: {{title: "{title}", description: "{description}" }}) {{
            ok,
            task {{
                id
            }}
        }} 
    }}''')
    assert result.errors is None
    assert result.data['createTask']['ok'] == True
    id = result.data['createTask']['task']['id']
    result = schema.execute(f'''query {{ 
        task (id: {id}) {{
            title, description, status
        }} 
    }}''')
    assert result.errors is None
    assert result.data['task']['description'] == description

