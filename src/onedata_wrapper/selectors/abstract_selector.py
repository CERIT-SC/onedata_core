import abc
from enum import Flag


class AbstractSelector(Flag):
    def convert(self, _conversion_table: dict["AbstractSelector": str] = None) -> list[str]:
        if _conversion_table is None:
            raise NotImplementedError("Abstract Selector must be filled in order to work")

        attributes_list = [_conversion_table[x] for x in _conversion_table if x in self]
        return attributes_list
