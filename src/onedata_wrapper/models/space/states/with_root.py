from onedata_wrapper.models.space.space_state import SpaceState
from onedata_wrapper.models.filesystem.dir_entry import DirEntry


class WithRoot(SpaceState):
    """
    Class representing the State of the Space class where root directory was initialized completely
    (with user-provided attributes).

    Space has `root_directory` object, which is reliably usable.
    """
    def __init__(self, root_dir: DirEntry):
        self._root_dir: DirEntry = root_dir
        super().__init__()

    @property
    def root_dir(self):
        return self._root_dir
