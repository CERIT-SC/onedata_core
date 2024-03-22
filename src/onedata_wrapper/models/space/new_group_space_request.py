from typing import Optional, Union
from onedata_wrapper.models.space.new_space_request import NewSpaceRequest


class NewGroupSpaceRequest(NewSpaceRequest):
    """
    Class representing New Group Space Request (under the specific group) when creating Space in Onedata

    Besides default parameters, NewGroupSpaceRequest must also have `group_id` in str
    """
    def __init__(self, name: str, group_id: str):
        if group_id is None or not isinstance(group_id, str):
            raise ValueError("GroupId must be of type str")

        self._group_id = group_id
        super().__init__(name)

    def request_attrs(self) -> dict[str, Union[str, bytes]]:
        out = super().request_attrs()

        additional = {
            "id": self.group_id
        }
        out.update(additional)

        return out

    @property
    def group_id(self):
        """Organization name of the Space
        """
        return self._group_id
