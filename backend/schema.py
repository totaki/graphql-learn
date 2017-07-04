import graphene
from store import JSONStore


class Status(graphene.Enum):
    TODO = 0
    STARTED = 1
    REVIEW = 2
    DONE = 4


class Task(graphene.ObjectType):

    title = graphene.String()
    description = graphene.String()
    status = Status()

    class Meta:
        interfaces = (graphene.relay.Node,)

    @classmethod
    def get_node(cls, id, context, info):
        data = context['store'].get(id)
        return Task(**data)


class CreateTask(graphene.relay.ClientIDMutation):

    class Input:
        title = graphene.String()
        description = graphene.String()

    ok = graphene.Boolean()
    task = graphene.Field(lambda: Task)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        index = context['store'].create({
            'title': args.get('title'),
            'description': args.get('description')}
        )
        data = context['store'].get(index)
        task = Task(status=Status.TODO, **data)
        ok = True
        return CreateTask(task=task, ok=ok)


class Mutations(graphene.ObjectType):
    create_task = CreateTask.Field()


class Query(graphene.ObjectType):

    tasks = graphene.relay.ConnectionField(Task)
    node = graphene.relay.Node.Field()

    def resolve_tasks(self, args, context, info):
        return sorted([int(k) for k in context['store'].all().keys()])


class Schema:

    def __init__(self, store: JSONStore) -> None:
        self.schema = graphene.Schema(query=Query, mutation=Mutations)
        self.store = store

    def execute(self, query: str) -> dict:
        return self.schema.execute(query, context_value={'store': self.store})
