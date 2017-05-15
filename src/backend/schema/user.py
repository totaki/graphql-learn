import graphene
from graphene import relay
from mappers import UserMapper


class User(graphene.ObjectType):
    """
    """

    class Meta:
        interfaces = (relay.Node, )

    firstname = graphene.String()
    lastname = graphene.String()

    @classmethod
    def get_node(cls, id, context, info):
        return cls('id', 'firstname', 'lastname')