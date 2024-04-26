
class PathFormatter:
    @staticmethod
    def symlink_absolute_path(space_id: str, file_path: str):
        """
        Formats space_id and file_path to a format required when creating a Symbolic link
        :param space_id: Onedata SpaceId
        :param file_path: absolute path to the file (with trailing slash /)
        :return:
        """
        # https://onedata.org/#/home/api/stable/oneprovider?anchor=operation/create_file
        if space_id == "" or file_path == "":
            raise ValueError("Neither of space id nor file path can be empty")

        return f"<__onedata_space_id:{space_id}>{file_path}"
