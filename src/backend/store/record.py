class RecordAttributeError(Exception):

    def __init__(self, keys):
        message = (
            'Dictionary key must be not exist in object attributes: %s'
            % keys
        )
        super().__init__(message)


class Record(object):

    exclude_dct_fields = ()

    def __init__(self, index, kind, data=None):
        self.id = index
        self.kind = kind
        self._data = {}
        if data:
            self._check_data_attributes(data)
            self._data = data

    def _check_data_attributes(self, data):
        keys = set(data.keys()).intersection(dir(self))
        if len(keys):
            raise RecordAttributeError(keys)

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        else:
            try:
                return super().__getattribute__(name)
            except AttributeError:
                return

    def update(self, **kwargs):
        self._check_data_attributes(kwargs)
        self._data.update(**kwargs)

    @property
    def as_dict(self):
        dct = {'id': self.id}
        dct.update(self._data)
        for field in self.exclude_dct_fields:
            if field in dct.keys():
                dct.pop(field)
        return dct
