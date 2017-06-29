import graphene


class Task(graphene.ObjectType):

    id = graphene.String()
    title = graphene.String()
    description = graphene.String()


class Query(graphene.ObjectType):

    test = graphene.Boolean()
    task = graphene.Field(Task, id=graphene.Int())

    def resolve_test(self, args, context, info):
        return True

    def resolve_task(self, args, context, info):
        id = args['id']
        data = context['store'].get(id)
        return Task(**data)


class Schema:

    def __init__(self, store):
        self.schema = graphene.Schema(query=Query)
        self.store = store

    def execute(self, query):
        return self.schema.execute(query, context_value={'store': self.store})
