from typing import Optional
from onedata_wrapper.models.space.space_state import SpaceState
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

    @property
    def space_id(self):
        return self._space_id

    @property
    def root_dir(self):
        return self._root_dir
