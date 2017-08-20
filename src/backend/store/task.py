from .record import Record


class TaskRecord(Record):

    exclude_dct_fields = ('iteration_id', 'parent_id')