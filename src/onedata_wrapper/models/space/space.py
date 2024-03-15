from typing import Optional
from onedata_wrapper.models.filesystem.dir_entry import DirEntry
from onedata_wrapper.models.space.space_state import SpaceState
from onedata_wrapper.models.space.states.inconsistent_root import InconsistentRoot
from onedata_wrapper.models.space.states.with_root import WithRoot
from onedata_wrapper.models.space.states.without_root import WithoutRoot


class Space:
    """
    Class representing Onedata Space.
    """
    def __init__(self, name: str, space_id: str, root_file_id: str, providers: list):
        self._state: SpaceState = WithoutRoot()

        self._name = name
        self._space_id = space_id
        self._root_file_id = root_file_id
        self._providers = providers

    def initialize_root(self):
        init_root_dir = DirEntry(file_id=self._root_file_id)
        self._state = InconsistentRoot(init_root_dir)

    def reinit_root(self, root_dir: DirEntry):
        if self._root_file_id != root_dir.file_id:
            raise ValueError("FileId of root does not match with FileId of space root")
        if not isinstance(root_dir, DirEntry):
            raise TypeError("Root directory is not of a type DirEntry")

        self._state = WithRoot(root_dir)

    def discard_root(self):
        self._state = WithoutRoot()

    @property
    def space_id(self) -> str:
        """Onedata SpaceId
        """
        if isinstance(self._state, InconsistentRoot):
            raise ValueError("Space in InconsistentRoot state")

        return self._space_id

    @property
    def name(self):
        """Name of the Space
        """
        if isinstance(self._state, InconsistentRoot):
            raise ValueError("Space in InconsistentRoot state")

        return self._name

    @property
    def root_dir(self) -> DirEntry:
        """
        DirEntry object representing root directory of the space.

        This object is accessible only if the state of the object is `WithRoot` or `InconsistentRoot`.
        """
        if isinstance(self._state, WithoutRoot):
            raise ValueError("Cannot return root directory of a space in state WithoutRoot")

        return self._state.root_dir
