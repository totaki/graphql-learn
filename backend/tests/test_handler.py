import json
import pytest


@pytest.mark.gen_test
def test_create_and_get_task(http_client, base_url):
    title = 'Title test'
    description = 'Create new task'
    create_body = f'''mutation {{
        createTask (data: {{title: "{title}", description: "{description}" }}) {{
            ok,
            task {{
                id
            }}
        }} 
    }}'''
    response = yield http_client.fetch(base_url + '/graphql', method='POST', body=create_body)
    index = int(json.loads(response.body.decode('utf-8'))['createTask']['task']['id'])
    get_body = f'''query {{ 
        task (id: {index}) {{
            title, description, status
        }} 
    }}'''
    response = yield http_client.fetch(base_url + '/graphql', method='POST', body=get_body)
    task = json.loads(response.body.decode('utf-8'))['task']
    assert task['description'] == description

