import logging as log
import os

import requests
from progress.bar import PixelBar

from page_loader import dom, errors, storage, url
from page_loader.cli import DEFAULT_OUTPUT


def download(page_url, output=DEFAULT_OUTPUT):
    log.info(f"Loading page {page_url}")
    html = load(page_url)
    log.debug(f"{page_url} loaded")

    html_path = os.path.join(output, url.to_file_name(page_url, ".html"))
    if os.path.exists(html_path):
        raise errors.SavingError(f"SavingError: '{html_path}' exists")

    dir_path = os.path.join(output, url.to_dir_name(page_url))
    if os.path.exists(dir_path):
        raise errors.SavingError(f"SavingError: '{dir_path}' exists")

    html_handled, resources = dom.prepare_html(html, page_url, dir_path)
    log.info(f"Saving page '{html_path}'")
    storage.save(html_handled, os.path.abspath(html_path))
    log.debug("HTML '{html_path}' saved")

    if resources:
        storage.create_directory(dir_path)
        log.debug(f"Directory '{dir_path}' created")
        log.info(f"Downloading resources from {page_url}")
        download_resources(resources)

    return html_path


def load(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        return response.text if response.encoding else response.content
    except requests.exceptions.RequestException as e:
        log.error(f"{link} not loaded")
        cause_info = (e.__class__, e, e.__traceback__)
        log.debug(str(e), exc_info=cause_info)
        raise errors.DownloadingError(f"{e} while loading {link}") from e


def download_resources(resources: dict):
    bar = PixelBar("\U0001F4E5 Downloading resources", max=len(resources))
    for resource_url, resource_path in resources.items():
        try:
            path = os.path.abspath(resource_path)

            content = load(resource_url)
            log.debug(f"{resource_url} loaded")

            storage.save(content, path)
            log.debug(f"'{resource_path}' saved")
        except (errors.DownloadingError, errors.SavingError):
            pass
        finally:
            bar.next()
    bar.finish()
