import pytest


@pytest.mark.gen_test
def test_create_and_get_task(http_client, base_url, get_response_field):
    title = 'Title test'
    description = 'Create new task'
    create_body = f'''mutation TaskMutation {{
        createTask (input: {{ title: "{title}", description: "{description}", clientMutationId:"abc" }}) {{
            ok,
            task {{
                id
            }}
        }} 
    }}'''
    response = yield http_client.fetch(base_url + '/graphql', method='POST', body=create_body)
    id = get_response_field(response, 'createTask', 'task', 'id')
    get_body = f'''query {{
        node (id : "{id}") {{
            id
            ... on Task {{
                title, description, status
            }}
        }} 
    }}'''
    response = yield http_client.fetch(base_url + '/graphql', method='POST', body=get_body)
    task = get_response_field(response, 'node')
    assert task['description'] == description

