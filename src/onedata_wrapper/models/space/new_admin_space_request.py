from typing import Optional, Union
from onedata_wrapper.models.space.new_space_request import NewSpaceRequest


class NewAdminSpaceRequest(NewSpaceRequest):
    """
    Class representing New Admin Space Request (global) when creating Space in Onedata

    Besides default parameters, NewAdminSpaceRequest can also have `description` in str and `organization_name` also
    in str
    """
    def __init__(self, name: str, description: Optional[str] = None, organization_name: Optional[str] = None):
        if description is not None and not isinstance(description, str):
            raise ValueError("Description must be of type str")
        if organization_name is not None and not isinstance(organization_name, str):
            raise ValueError("Organization name must be of type str")

        self._description = description
        self._organization_name = organization_name

        super().__init__(name)

    def request_attrs(self) -> dict[str, Union[str, bytes]]:
        out = super().request_attrs()

        if self.description is not None:
            out["description"] = self.description

        if self.organization_name is not None:
            out["organization_name"] = self.organization_name

        return out

    @property
    def description(self):
        """Description of the Space
        """
        return self._description

    @property
    def organization_name(self):
        """Organization name for the Space
        """
        return self._organization_name
