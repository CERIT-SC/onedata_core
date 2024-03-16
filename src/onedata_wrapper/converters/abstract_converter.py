import abc
from abc import ABC


class AbstractConverter(ABC):
    """
    Class representing Abstract Converter

    Converters are used to convert onedata-lib object into object understandable by this library.
    Each descendant of this class must implement convert() function with exactly one parameter; object to convert.
    The return value of convert() function is an object from models package of this library
    """
    @staticmethod
    @abc.abstractmethod
    def convert(object_to_convert):
        """
        Converts onedata-lib object to object from models package
        :param object_to_convert: Onedata-lib object
        :return: Object from models package of this library
        """
        raise NotImplementedError("This function must be implemented for all the inherited classes")
