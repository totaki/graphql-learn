import graphene
from store import JSONStore


class Status(graphene.Enum):
    TODO = 0
    STARTED = 1
    REVIEW = 2
    DONE = 4


class Task(graphene.ObjectType):

    id = graphene.String()
    title = graphene.String()
    description = graphene.String()
    status = Status()


class TaskInput(graphene.InputObjectType):
    title = graphene.String()
    description = graphene.String()


class CreateTask(graphene.Mutation):

    class Input:
        data = graphene.Argument(TaskInput)

    ok = graphene.Boolean()
    task = graphene.Field(lambda: Task)

    @staticmethod
    def mutate(root, args, context, info):
        index = context['store'].create(**args)
        data = context['store'].get(index)
        task = Task(status=Status.TODO, **data)
        ok = True
        return CreateTask(task=task, ok=ok)


class Mutations(graphene.ObjectType):
    create_task = CreateTask.Field()


class Query(graphene.ObjectType):

    test = graphene.Boolean()
    task = graphene.Field(Task, id=graphene.Int())

    def resolve_test(self, args, context, info) -> bool:
        return True

    def resolve_task(self, args, context, info) -> Task:
        id = args['id']
        data = context['store'].get(id)
        return Task(**data)


class Schema:

    def __init__(self, store: JSONStore) -> None:
        self.schema = graphene.Schema(query=Query, mutation=Mutations)
        self.store = store

    def execute(self, query: str) -> dict:
        return self.schema.execute(query, context_value={'store': self.store})
