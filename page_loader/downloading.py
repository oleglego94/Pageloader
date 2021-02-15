import logging as log
import os

import requests
from progress.bar import PixelBar

from page_loader import dom, errors, storage, url
from page_loader.cli import DEFAULT_OUTPUT


def download(page_url, output=DEFAULT_OUTPUT):
    log.info("Downloading page")
    html = load(page_url)
    log.debug(f"{page_url} downloaded")

    html_path = os.path.join(output, url.to_file_name(page_url, ".html"))
    if os.path.exists(html_path):
        raise errors.SavingError(f"SavingError: '{html_path}' exists")

    dir_path = os.path.join(output, url.to_dir_name(page_url))
    if os.path.exists(dir_path):
        raise errors.SavingError(f"SavingError: '{dir_path}' exists")

    html_handled, resources = dom.prepare_html(html, page_url, dir_path)
    log.info("Saving page")
    storage.save(html_handled, os.path.abspath(html_path))
    log.debug("Handled HTML saved")

    if resources:
        storage.create_directory(dir_path)
        log.debug("Directory created")
        log.info("Downloading resources")
        download_resources(resources)

    return html_path


def load(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        return response.text if response.encoding else response.content
    except requests.exceptions.RequestException as e:
        log.error(f"{link} not downloaded")
        raise errors.DownloadingError(f"{e} while downloading {link}") from e


def download_resources(resources: dict):
    bar = PixelBar("\U0001F4E5 Downloading resources", max=len(resources))
    for resource_url, resource_path in resources.items():
        try:
            path = os.path.abspath(resource_path)

            content = load(resource_url)
            log.debug(f"{resource_url} downloaded")

            storage.save(content, path)
            log.debug(f"'{resource_path}' saved")
        except (errors.DownloadingError, errors.SavingError):
            pass
        finally:
            bar.next()
    bar.finish()
