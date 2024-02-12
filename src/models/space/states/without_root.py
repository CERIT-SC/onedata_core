from models.space.space_state import SpaceState


class WithoutRoot(SpaceState):
    def __init__(self):
        super().__init__()
