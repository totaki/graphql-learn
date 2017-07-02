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
    # board = graphene.Int()

    class Meta:
        interfaces = (graphene.relay.Node,)

    @classmethod
    def get_node(cls, id, context, info):
        data = context['store'].task.get(id)
        return Task(**data)


class CreateTask(graphene.relay.ClientIDMutation):

    class Input:
        title = graphene.String()
        description = graphene.String()

    ok = graphene.Boolean()
    task = graphene.Field(lambda: Task)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        index = context['store'].task.create({
            'title': args.get('title'),
            'description': args.get('description')}
        )
        data = context['store'].task.get(index)
        task = Task(status=Status.TODO, **data)
        ok = True
        return CreateTask(task=task, ok=ok)


class Mutations(graphene.ObjectType):
    create_task = CreateTask.Field()


class Board(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.relay.Node,)

    title = graphene.String(description='Board view name')
    tasks = graphene.relay.ConnectionField(Task, description='All tasks for this board')

    @classmethod
    def get_node(cls, id, context, info):
        data = context['store'].board.create(id)
        tasks = filter(lambda t: t['board'] == id, context['store'].task.all())
        return Board(id=id, tasks=[t['id'] for t in tasks], **data)

    def resolve_tasks(self, args, context, info):
        tasks = [context['store'].task.get(t) for t in self.tasks]
        return [Task(**data) for data in tasks]


class Query(graphene.ObjectType):

    test = graphene.Boolean()
    # board = graphene.Field(Board, id=graphene.Int())
    node = graphene.relay.Node.Field()

    def resolve_test(self, args, context, info) -> bool:
        return True

    # def resolve_board(self, args, context, info) -> Task:
    #     id = args['id']
    #     data = context['store'].board.get(id)
    #     return Board(**data)


class Schema:

    def __init__(self, store: JSONStore) -> None:
        self.schema = graphene.Schema(query=Query, mutation=Mutations)
        self.store = store

    def execute(self, query: str) -> dict:
        return self.schema.execute(query, context_value={'store': self.store})
