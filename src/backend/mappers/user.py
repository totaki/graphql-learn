"""
>>> user = UserMapper(1, 'mail', 'password', 'James', 'Bond')
>>> user.id
1
>>> user.firstname
'James'
"""
from .base import BaseMapper


class UserMapper(BaseMapper):
    """UserMapper
    """

    fields = (
        'id',
        'email',
        'password_hash',
        'firstname',
        'lastname',
    )
