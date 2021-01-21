import requests
from page_loader import io


def save(source, file_path):
    response = requests.get(source)
    return io.write_file(response.content, file_path)
