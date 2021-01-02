import os
import re
import requests
from page_loader.cli import DEFAULT_DIR


def download(url, directory=DEFAULT_DIR):
    file_name = convert(url)
    path = os.path.join(directory, file_name)
    page = requests.get(url)
    with open(path, "wb") as file:
        file.write(page.content)
    os.chdir(directory)
    return os.path.join(os.getcwd(), file_name)


def convert(url):
    if url.endswith("/"):
        url = url[:-1]
    match = re.split(".*://", url)
    name = re.sub(r"\W", "-", match[1])
    return name + ".html"
