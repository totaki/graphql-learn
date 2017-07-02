def test_test_schema(schema):
    result = schema.execute('query { test }')
    assert not result.errors
    assert result.data['test']


def test_create_and_get_task(schema):
    title = 'Title test'
    description = 'Create new task'
    result = schema.execute(f'''mutation {{
        createTask (input: {{title: "{title}", description: "{description}", clientMutationId:"abc" }}) {{
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
        node (id : "{id}") {{
            id
            ... on Task {{
                title, description, status
            }}
        }} 
    }}''')
    assert result.errors is None
    assert result.data['node']['description'] == description

