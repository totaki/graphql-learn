"""
>>> from graphene.test import Client
>>> schema = graphene.Schema(query=Query)
>>> client = Client(schema)
>>> result = client.execute('''
...     user(id: 1) {
...         firstname,
...         lastname,
...     }
... ''')
>>> result
6
"""

import graphene
from .user import User

class Query(graphene.ObjectType):
    
    user = graphene.Field(User)
