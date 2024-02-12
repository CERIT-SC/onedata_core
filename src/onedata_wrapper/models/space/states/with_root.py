from onedata_wrapper.models.space.space_state import SpaceState
from onedata_wrapper.models.filesystem.dir_entry import DirEntry


class WithRoot(SpaceState):
    def __init__(self, root_dir: DirEntry):
        self._root_dir: DirEntry = root_dir
        super().__init__()

    @property
    def root_dir(self):
        return self._root_dir
