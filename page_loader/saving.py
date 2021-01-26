import requests
from page_loader import io
from page_loader.logging import setup_logging

setup_logging()


def save(source, file_path):
    try:
        response = requests.get(source)
        code = response.status_code
        if code == requests.codes.ok:
            io.write_file(response.content, file_path)
        else:
            response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise error
