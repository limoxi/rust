from functools import reduce
from typing import Self

def _empty_map():
    return Map({})

def _walk_data(data, key):
    """
    遍历data
    如果data是列表，则赋值为第一个元素
    """
    if isinstance(data, list):
        if len(data) > 0:
            data = data[0]
        else:
            data = {}

    return data.get(key, {})


class Map:
    __slots__ = ('__dict_data',)
    def __init__(self, dict_data):
        self.__dict_data = dict_data

    def get_raw(self, path=None):
        if path is None:
            return self.__dict_data

        v = reduce(_walk_data, path.split("."), self.__dict_data)
        if isinstance(v, dict) and len(v) == 0:
            return None
        return v

    def get_str(self, path, default='') -> str:
        v = self.get_raw(path)
        if v is None or isinstance(v, (list, dict)):
            return default

        return str(v)

    def get_int(self, path, default=0) -> int:
        v = self.get_raw(path)
        if v is None or isinstance(v, (list, dict)):
            return default

        return int(v)

    def get_float(self, path, default=0.0) -> float:
        v = self.get_raw(path)
        if v is None or isinstance(v, (list, dict)):
            return default

        return float(v)

    def get_bool(self, path, default=False) -> bool:
        v = self.get_raw(path)
        if v is None or isinstance(v, (list, dict)):
            return default

        return bool(v)

    def get_map(self, path, default=None) -> Self:
        v = self.get_raw(path)
        if v is not None and isinstance(v, list) and len(v) > 0:
            return Map(v[0])

        if v is None or not isinstance(v, dict):
            if default is None:
                return _empty_map()
            return Map(default)

        return Map(v)

    def get_dict(self, path, default=None) -> dict:
        v = self.get_raw(path)
        if v is not None and isinstance(v, list) and len(v) > 0:
            return v[0]

        if v is None or not isinstance(v, dict):
            if default is None:
                return {}
            return default

        return v

    def get_list(self, path, default=None) -> []:
        v = self.get_raw(path)
        if v is None or not isinstance(v, list):
            if default is None:
                return []
            return default
        return v