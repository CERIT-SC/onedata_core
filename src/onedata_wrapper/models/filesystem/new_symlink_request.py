from typing import Optional, Union
from onedata_wrapper.models.filesystem.dir_entry import DirEntry
from onedata_wrapper.models.filesystem.entry_request import EntryRequest
from onedata_wrapper.models.filesystem.new_entry_request import NewEntryRequest
from onedata_wrapper.models.space.space import Space
from onedata_wrapper.models.space.space_request import SpaceRequest
from onedata_wrapper.utils.formatters import PathFormatter


class NewSymlinkRequest(NewEntryRequest):
    """
    Class representing New Symbolic link Entry Request when creating Entry in Onedata

    Besides default parameters, NewSymlinkEntry must also have a string `target_file_path` (symlink value),
    which assigns the path to the symlink

    The `target_file_path` attribute can contain either relative or absolute path. If the path is absolute, it must
    contain prefix in format of `<__onedata_space_id:$SPACE_ID>/` where `$SPACE_ID` is id of an actual space.
    For this purpose, the class method `from_absolute()` should be used.

    Yet the interspace links do not work.
    """
    def __init__(self, parent: Union[DirEntry, EntryRequest], name: str, target_file_path: str, mode: int = 644):
        self._value = target_file_path
        super().__init__(parent, name, mode)

    @classmethod
    def from_absolute(cls, parent: Union[DirEntry, EntryRequest], name: str, space: Union[Space, SpaceRequest],
                      absolute_path: str, mode: int = 644):
        """This method allows using a Space or SpaceRequest object and the file absolute path
        for creation of the symlink with an absolute path
        """
        return cls(parent, name, PathFormatter.symlink_absolute_path(space.space_id, absolute_path), mode)

    def request_attrs(self) -> dict[str, Union[str, bytes]]:
        out = super().request_attrs()
        additional = {
            "type": "SYMLNK",
            "target_file_path": self._value
        }
        out.update(additional)

        return out

    @property
    def value(self):
        """Link to the requested file (target file path / symlink value)
        """
        return self._value
