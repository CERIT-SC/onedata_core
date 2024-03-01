
class SpaceRequest:
    def __init__(self, space_id: str):
        self._space_id: str = space_id

    @property
    def space_id(self):
        return self._space_id
