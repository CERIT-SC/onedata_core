from .file_attributes_converter import FileAttributesConverter
from converters.abstract_converter import AbstractConverter
from models.filesystem.filesystem_entry import FilesystemEntry
from oneprovider_client.models.directory_children import DirectoryChildren


class DirectoryChildrenConverter(AbstractConverter):
    @staticmethod
    def convert(children: DirectoryChildren) -> list[FilesystemEntry]:
        converted_children = []
        for child in children.children:
            converted_child = FileAttributesConverter.convert(child)
            converted_children.append(converted_child)

        return converted_children
