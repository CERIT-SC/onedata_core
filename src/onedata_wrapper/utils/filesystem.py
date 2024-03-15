from typing import Optional


def read_file_contents(path: str) -> Optional[str]:
    """
    Reads the contents of the file given by path.
    The read is processed textually ('r' is passed as an argument to open).
    :param path: String representing a path to the file
    :return: String contents of the file or None if any Exception occurred
    """
    try:
        with open(path, "r") as f:
            return f.read()
    except (IOError, Exception):
        return None
