import logging
import os
from page_loader import io
from page_loader.logging import setup_logging
from page_loader.cli import DEFAULT_DIR
from page_loader.naming import make_name
from page_loader.resources import get_local_resources
from page_loader.saving import save

setup_logging()


def download(url, directory=DEFAULT_DIR):
    logging.info("Downloading html")
    page = download_page(url, directory)

    logging.info("Downloading resources")
    download_resources(page, url, directory)
    return page


def download_page(source, storage):
    html_name = make_name(source, ".html")
    html_path = os.path.join(storage, html_name)
    save(source, html_path)
    logging.info(f"{source} was successfully downloaded into '{html_name}'")
    return os.path.abspath(html_path)


def download_resources(html_path, source, storage):
    resources_dir = make_name(source, "_files")
    resources_path = os.path.join(storage, resources_dir)
    os.mkdir(resources_path)
    logging.info(f"{resources_dir} was successfully created")
    new_html = get_local_resources(html_path, resources_path, source)
    rewrite_html(new_html, html_path)
    return os.path.abspath(resources_path)


def rewrite_html(html, path):
    io.write_file(html, path, "w")
    logging.info(f"Links in {path} were successfully changed")
