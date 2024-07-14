from typing import Self
from .serializable import Serializable


class ConstraintData(Serializable):
    def __init__(self, name: str) -> Self:
        self.name = name

    def serialize(self):
        raise NotImplementedError("This method should be implemented by subclasses")
