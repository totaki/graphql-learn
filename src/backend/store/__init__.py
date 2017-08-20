from .in_memory_store import InMemoryStore
from .task import TaskRecord


class Store(InMemoryStore):

    def create_task(self, data=None, **kwargs):
        return self.create(
            'task', data=data, record_class=TaskRecord, **kwargs
        )

    def create_iteration(self, data=None, **kwargs):
        return self.create('iteration', data=data, **kwargs)

    @property
    def tasks(self):
        return self.all_by_kind('task')

    @property
    def iterations(self):
        return self.all_by_kind('iteration')