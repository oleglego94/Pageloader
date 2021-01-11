import re
import os
import requests
from page_loader.cli import DEFAULT_DIR


def download_page(url, directory=DEFAULT_DIR):
    response = requests.get(url)
    name = convert_url(url)

    html_path = os.path.join(directory, name + ".html")
    with open(html_path, "wb") as f:
        f.write(response.content)

    return os.path.abspath(html_path)


def convert_url(url):
    if url.endswith("/"):
        url = url[:-1]
    match = re.split(".*://", url)
    return re.sub(r"\W", "-", match[1])
