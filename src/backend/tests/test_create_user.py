import pytest
from main import SyncTarantoolConnection


@pytest.fixture(scope='module')
def tarantool_connection():
    with SyncTarantoolConnection.connect_from_settings() as conn:
        return conn


def test_create_user_with_tarantool_sync(tarantool_connection):
    space = tarantool_connection.space('user')
    user_data = [1, 'field1', 'field2', 'field3', 'field3']
    space.insert(user_data)
    returned_user_data = space.select((1,))
    space.delete((1,))
    assert user_data == returned_user_data.data[0]
    tarantool_connection.close()
