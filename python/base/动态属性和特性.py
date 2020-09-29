import keyword
from urllib.request import urlopen
import warnings
import os
import json

URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = 'data/osconfeed.json'


def load():
    if not os.path.exists(JSON):
        msg = f'downloading {URL} to {JSON}'
        warnings.warn(msg)
        with urlopen(URL) as remote, open(JSON, 'wb') as local:
            # 两个上下文管理器
            local.write(remote.read())
    with open(JSON) as fp:
        return json.load(fp)


# AttrDict (https://pypi.python.org/pypi/attrdict)
# addDict (https://pypi.python.org/pypi/addict)
from collections import abc


class FrozenJson:
    """一个只读接口，使用属性表示法访问JSON类对象
    """

    def __init__(self, mapping: dict):
        # self.__data = dict(mapping)
        # x.class # SyntaxError ==> x_
        # x.2be # SyntaxError   ==> attr_0
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJson.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableMapping):
            return [cls.build(item) for item in obj]
        else:
            return obj


if __name__ == '__main__':
    # print(load())
    pass
