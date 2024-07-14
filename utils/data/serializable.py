from typing import Self


class Serializable:
    def __init__(self) -> Self:
        pass
    
    def serialize(self) -> dict:
        raise NotImplementedError("This method should be implemented by subclasses")

    def deserialize(data) -> Self:
        raise NotImplementedError("This method should be implemented by subclasses")
