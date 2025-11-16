from enum import IntEnum


class IntEnumWithLabels(IntEnum):
    def __new__(cls, value: int, label: str):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj
