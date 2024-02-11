import sqlalchemy


class File:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_json(self):
        res = self.__dict__.copy()
        res['created_at'] = res['created_at'].timestamp()
        return res
