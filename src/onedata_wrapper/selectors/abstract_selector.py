import abc
from enum import Flag


class AbstractSelector(Flag):
    def convert(self, _conversion_table: dict["AbstractSelector": str] = None) -> list[str]:
        """
        Takes parameters given by user selection from Selector and convert them to the list of string representation
        of these parameters based on the conversion table
        :param _conversion_table: Dictionary conversion table from set Selector to set of strings
        :return: List of strings representing actual Selector selection
        """
        if _conversion_table is None:
            raise NotImplementedError("Abstract Selector must be filled in order to work")

        attributes_list = [_conversion_table[x] for x in _conversion_table if x in self]
        return attributes_list
