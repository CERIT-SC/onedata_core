
def read_file_contents(path: str):
    try:
        with open(path, "r") as f:
            return f.read()
    except (IOError, Exception):
        return None
