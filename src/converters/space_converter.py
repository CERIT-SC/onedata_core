from oneprovider_client.models.space import Space as OneproviderSpace
from converters.abstract_converter import AbstractConverter
from models.space.space import Space
from models.filesystem.dir_entry import DirEntry


class SpaceConverter(AbstractConverter):
    @staticmethod
    def convert(oneprovider_space: OneproviderSpace) -> Space:
        # changed
        entry_root_dir = DirEntry(file_id=oneprovider_space.space_id)
        # unchanged
        entry_name = oneprovider_space.name
        entry_space_id = oneprovider_space.space_id
        entry_providers = oneprovider_space.providers

        space = Space(entry_name, entry_space_id, entry_root_dir, entry_providers)
        return space
