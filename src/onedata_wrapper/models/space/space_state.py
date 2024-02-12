from abc import ABC


class SpaceState(ABC):
    def __init__(self):
        raise NotImplementedError("This function must be implemented for all the inherited classes")
