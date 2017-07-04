import pytest


CREATE_TASK_TITLE = 'Title test'
CREATE_TASK_DESCRIPTION = 'Create new task'
CREATE_TASK_QUERY = f'''mutation TaskMutation {{
        createTask (input: {{ title: "{CREATE_TASK_TITLE}", description: "{CREATE_TASK_DESCRIPTION}", clientMutationId:"abc" }}) {{
            ok,
            task {{
                id
            }}
        }} 
    }}'''


@pytest.mark.gen_test
def test_create_and_get_tasks(http_client, base_url, get_response_field):
    ids = []
    for i in range(10):
        response = yield http_client.fetch(
            base_url + '/graphql', method='POST', body=CREATE_TASK_QUERY)
        id = get_response_field(response, 'createTask', 'task', 'id')
        ids.append(id)
    get_body = f'''query {{
        node (id : "{ids[0]}") {{
            id
            ... on Task {{
                title, description, status
            }}
        }} 
    }}'''
    response = yield http_client.fetch(base_url + '/graphql', method='POST', body=get_body)
    task = get_response_field(response, 'node')
    assert task['description'] == CREATE_TASK_DESCRIPTION

    get_all_paginated_query = f'''query {{
        tasks (first : 5) {{
            pageInfo {{
                startCursor
                endCursor
                hasNextPage
                hasPreviousPage
            }}
            edges {{
                cursor
                node {{
                    title
                }}
            }}
        }}
    }}'''
    response = yield http_client.fetch(base_url + '/graphql', method='POST', body=get_all_paginated_query)
    assert get_response_field(response, 'tasks', 'pageInfo', 'hasNextPage')
    assert not get_response_field(response, 'tasks', 'pageInfo', 'hasPreviousPage')

    cursor = get_response_field(response, 'tasks', 'edges')[2]['cursor']
    last_cursor = get_response_field(response, 'tasks', 'edges')[4]['cursor']
    get_all_paginated_query = f'''query {{
        tasks (first : 2, after: "{cursor}") {{
            pageInfo {{
                startCursor
                endCursor
                hasNextPage
                hasPreviousPage
            }}
            edges {{
                cursor
                node {{
                    title
                }}
            }}
        }}
    }}'''
    response = yield http_client.fetch(base_url + '/graphql', method='POST', body=get_all_paginated_query)
    cursor_last = get_response_field(response, 'tasks', 'edges')[1]['cursor']
    assert cursor_last == last_cursor


