import os


def write_file(content, path, mode="wb"):
    try:
        with open(path, mode) as f:
            f.write(content)
        return path
    except OSError:
        raise


def read_file(path, mode="r"):
    try:
        with open(path, mode) as f:
            content = f.read()
        return content
    except OSError:
        raise


def create_directory(path):
    try:
        os.mkdir(path)
    except OSError:
        raise
