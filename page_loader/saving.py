import requests

from page_loader import io
from page_loader.logging import setup_logging

setup_logging()


def save(source, file_path):
    try:
        response = requests.get(source)
        response.raise_for_status()
        io.write_file(response.content, file_path)

    except requests.exceptions.ConnectionError as error:
        raise error
