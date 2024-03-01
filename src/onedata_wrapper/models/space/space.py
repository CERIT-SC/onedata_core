from typing import Optional

from onedata_wrapper.models.filesystem.dir_entry import DirEntry
from onedata_wrapper.models.space.space_state import SpaceState
from onedata_wrapper.models.space.states.inconsistent_root import InconsistentRoot
from onedata_wrapper.models.space.states.with_root import WithRoot
from onedata_wrapper.models.space.states.without_root import WithoutRoot


class Space:
    def __init__(self, name=None, space_id=None, root_file_id=None, providers=None):
        self._name: Optional[str] = None
        self._space_id: Optional[str] = None
        self._root_file_id: Optional[str] = None
        self._providers: Optional[list[tuple]] = None
        self._state: SpaceState = WithoutRoot()

        if name is not None:
            self._name = name

        if space_id is not None:
            self._space_id = space_id

        if root_file_id is not None:
            self._root_file_id = root_file_id

        if providers is not None:
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
    def space_id(self):
        if isinstance(self._state, InconsistentRoot):
            raise ValueError("Space in InconsistentRoot state")

        return self._space_id

    @property
    def name(self):
        if isinstance(self._state, InconsistentRoot):
            raise ValueError("Space in InconsistentRoot state")

        return self._name

    @property
    def root_dir(self) -> DirEntry:
        if isinstance(self._state, WithoutRoot):
            raise ValueError("Cannot return root directory of a space in state WithoutRoot")

        return self._state.root_dir
