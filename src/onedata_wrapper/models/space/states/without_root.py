from onedata_wrapper.models.space.space_state import SpaceState


class WithoutRoot(SpaceState):
    """
    Class representing the State of the Space class where root directory was not yet requested and Space has no
    `root_directory` object.
    """
    def __init__(self):
        super().__init__()
