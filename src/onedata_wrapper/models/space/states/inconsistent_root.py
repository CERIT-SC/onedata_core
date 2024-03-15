from onedata_wrapper.models.space.space_state import SpaceState
from onedata_wrapper.models.filesystem.dir_entry import DirEntry


class InconsistentRoot(SpaceState):
    """
    Class representing the State of the Space class where root directory was not yet initialized
    but request for the initialization was provided and not yet finished.

    Space has `root_directory` object, however, it is not initialized properly and has an inconsistent state.
    """
    def __init__(self, root_dir: DirEntry):
        self._root_dir: DirEntry = root_dir
        super().__init__()

    @property
    def root_dir(self):
        return self._root_dir
