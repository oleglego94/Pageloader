import os
from page_loader.cli import DEFAULT_DIR
from page_loader.naming import make_name
from page_loader.resources import get_local_resources
from page_loader.saving import save


def download(url, directory=DEFAULT_DIR):
    page = download_page(url, directory)
    download_resources(page, url, directory)
    return page


def download_page(source, storage):
    html_name = make_name(source, ".html")
    html_path = os.path.join(storage, html_name)

    save(source, html_path)
    return os.path.abspath(html_path)


def download_resources(html_path, source, storage):
    resources_dir = make_name(source, "_files")
    resources_path = os.path.join(storage, resources_dir)
    os.mkdir(resources_path)

    get_local_resources(html_path, resources_path, source)
    return os.path.abspath(resources_path)
