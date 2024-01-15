import abc
from abc import ABC


class AbstractConverter(ABC):
    @staticmethod
    @abc.abstractmethod
    def convert(object_to_convert):
        pass
