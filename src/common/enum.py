from enum import Enum


class BaseEnum(Enum):
    def __init__(self, value, description):
        self._value_ = value
        self._description = description

    @property
    def description(self) -> str:
        return self._description
