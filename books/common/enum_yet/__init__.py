# coding: utf-8
"""
Enum对象，由于python 提供的包enum34中的Enum、IntEnum在使用过程中容易出现忘记加.value后缀等情况，非常容易出现bug，比如在落库的时候，Enum类型
的数据在做In判断的时候，都十分的容易出错，故此自己开发了一套Enum。本着使用简单的原则，防了Enum34中的概念，加之__choices__的概念，做了如下实现，自带验证功能。

使用方式与头条系统中的enum34几乎没有差别，使用方式如下。
class Example(Enum):
    a = 1
    b = 2

    __choices__ = (
        (a, u'测试样例a'),
        (b, u'测试样例b'),
    )


>> Example['a']  # 通过名字来找到值
Out: 1
>> Example[1]  # 通过值来找到值
Out: 1
>> c = Example[3]
Out: ValueError: 3
>> c = Example['c']
Out: KeyError: c

>> a1 = Example[1]
>> print a1
Out: 1
>> a1.label
Out: u'测试样例a'
>> a1.name
Out: a

"""
from __future__ import unicode_literals


class NewInt(int):
    """为了能够给int赋予各种属性，比如说label,value等属性"""


class NewStr(str):
    """为了能够给str赋予各种属性，比如说label,value等属性"""


class EnumMeta(type):
    __choices__ = ()
    _enum_type = NewInt

    def __new__(mcs, *args, **kwargs):
        obj = type.__new__(mcs, *args, **kwargs)
        obj._value_to_label = dict(obj.__choices__)  # label
        obj._keys, obj._values = [], []
        for key, value in obj.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, (int, str)):
                    val = obj._enum_type(value)
                    val.name = key
                    val.value = value    # todo wangtao 兼容.value形式，以后逐渐废除
                    val.label = obj._value_to_label.get(val) or key
                    setattr(obj, key, val)
                    obj._keys.append(key)
                    obj._values.append(val)

        if len(set(obj._keys)) != len(set(obj._values)):  # 确保不会有重复
            raise ValueError('duplicate value')
        return obj

    def __getitem__(self, key):
        """可以根据name和value获取"""
        for val in self._values:
            if val == key:
                return val

        if key in self._keys:
            return getattr(self, key, None)
        raise KeyError(key)

    def __setattr__(cls, key, value):
        if not key.startswith('_') and key in cls._keys:
            raise AttributeError('Cannot reassign members')
        return super(EnumMeta, cls).__setattr__(key, value)


class EnumMixin(object):
    __choices__ = ()

    @classmethod
    def to_dict(cls):
        if not getattr(cls, '_to_dict', None):
            cls._to_dict = dict((x.name, x.value) for x in cls._values)
        return cls._to_dict

    @classmethod
    def label_items(cls):
        return cls.__choices__

    @classmethod
    def get_choices(cls):
        return cls.__choices__

    @classmethod
    def get_display_name(cls, value):
        return cls[value].label

    @classmethod
    def all_elements(cls):
        return cls._values

    # 使用 Enum.name('name') / Enum.value(1) 的形式替代  Enum['name'] , Enum[1]
    @classmethod
    def name(cls, name):
        res = getattr(cls, name)
        if res is None:
            raise KeyError(name)
        return res

    @classmethod
    def value(cls, value):
        for val in cls._values:
            if val == value:
                return val
        else:
            raise ValueError(value)

    def __new__(cls, enum_value):
        return cls[enum_value]


class Enum(EnumMixin):
    __metaclass__ = EnumMeta
    _enum_type = NewStr


class IntEnum(EnumMixin):
    __metaclass__ = EnumMeta
    _enum_type = NewInt
