import os

from page_loader import url


def save(content, path):
    try:
        if isinstance(content, bytes):
            mode = "wb"
        else:
            mode = "w"
        with open(path, mode) as f:
            f.write(content)
    except OSError:
        raise


def create_directory(path):
    try:
        os.mkdir(path)
    except OSError:
        raise


def make_file_path(link, dir_path):
    path, ext = os.path.splitext(link)
    if not ext:
        ext = ".html"
    file_name = url.to_file_name(path, ext)
    path = os.path.join(dir_path, file_name)
    _, directory = os.path.split(dir_path)
    rel_path = os.path.join(directory, file_name)
    return path, rel_path
