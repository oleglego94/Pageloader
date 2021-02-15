import logging as log
import os

from page_loader import errors


def save(content, path):
    try:
        if isinstance(content, bytes):
            mode = "wb"
        else:
            mode = "w"

        with open(path, mode) as f:
            f.write(content)
    except OSError as e:
        log.error(f"'{path}' not saved")
        raise errors.SavingError(f"{e} while saving '{path}'") from e


def create_directory(path):
    try:
        os.mkdir(path)
    except OSError as e:
        log.error(f"Directory '{path}' not created")
        raise errors.SavingError(f"{e} while creating '{path}'") from e
