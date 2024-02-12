import abc
from abc import ABC


class AbstractConverter(ABC):
    @staticmethod
    @abc.abstractmethod
    def convert(object_to_convert):
        raise NotImplementedError("This function must be implemented for all the inherited classes")
