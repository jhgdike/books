# -*- coding: utf-8 -
"""
自定义的MySQL 的Column，为了支持MySQL不支持的复杂类型
Reference: https://yiyibooks.cn/wizard/sqlalchemy_11/orm_extensions_mutable.html
"""

from __future__ import unicode_literals

from sqlalchemy.types import TypeDecorator, VARCHAR
from sqlalchemy.ext.mutable import Mutable
import json


class JSONEncodedDict(TypeDecorator):
    """Representes an immutable structure as a json-encoded string"""

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value:
            value = json.loads(value)
        return value or dict()

    # 不一定对，下面这两个函数。如果不对，可以删去
    def process_literal_param(self, value, dialect):
        pass

    @property
    def python_type(self):
        return str


class MutableDict(Mutable, dict):

    @classmethod
    def coerce(cls, key, value):
        """Convert plain dictionaries to MutableDict"""

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        """Detect dictionary set events and emit change events"""

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        """Detect dictionary del events and emit change events"""

        dict.__delitem__(self, key)
        self.changed()


MutableDict.associate_with(JSONEncodedDict)
