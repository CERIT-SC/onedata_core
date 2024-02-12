from models.space.space_state import SpaceState
from models.filesystem.dir_entry import DirEntry


class WithRoot(SpaceState):
    def __init__(self, root_dir: DirEntry):
        self._root_dir: DirEntry = root_dir
        super().__init__()

    @property
    def root_dir(self):
        return self._root_dir
