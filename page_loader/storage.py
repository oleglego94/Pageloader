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
        cause_info = (e.__class__, e, e.__traceback__)
        log.debug(str(e), exc_info=cause_info)
        raise errors.SavingError(f"{e} while saving '{path}'") from e


def create_directory(path):
    try:
        os.mkdir(path)
    except OSError as e:
        log.error(f"Directory '{path}' not created")
        cause_info = (e.__class__, e, e.__traceback__)
        log.debug(str(e), exc_info=cause_info)
        raise errors.SavingError(f"{e} while creating '{path}'") from e
