import logging
import os
from urllib import parse

from bs4 import BeautifulSoup
from progress.spinner import PixelSpinner as Spinner

from page_loader.logging import setup_logging
from page_loader.naming import make_name
from page_loader.saving import save

RESOURCES = {
    "img": "src",
    "link": "href",
    "script": "src",
}

setup_logging()


def get_local_resources(html_path, directory, url):
    soup = make_soup(html_path)
    spinner = Spinner("Downloading resources ")
    for resource in RESOURCES.keys():
        tags = soup.find_all(resource)
        attr = RESOURCES[resource]
        get_resource(tags, attr, url, directory)
        spinner.next()
    spinner.finish()
    return soup.prettify(formatter="html5")


def get_resource(tags, attr, url, directory):

    for tag in tags:
        link = tag.get(attr)
        if not link:
            continue
        else:
            normal_link = normalize_link(link, url)
            if not is_local(normal_link, url):
                continue
            else:
                path, rel_path = make_file_path(normal_link, directory)
                save(normal_link, path)
                logging.info(
                    f"{normal_link} was successfully downloaded into '{rel_path}'"  # noqa: E501
                )
                tag[attr] = rel_path
    return tags


def get_domain(url):
    parsed_url = parse.urlparse(url)
    scheme = parsed_url.scheme
    host = parsed_url.netloc
    return "{}://{}".format(scheme, host)


def make_soup(doc_path):
    with open(doc_path) as fp:
        soup = BeautifulSoup(fp, "html.parser")
    return soup


def normalize_link(link, page_url):
    domain = get_domain(page_url)
    parsed_url = parse.urlparse(link)
    without_domain = not parsed_url.scheme and not parsed_url.netloc
    if without_domain and parsed_url.path.startswith("/"):
        return parse.urljoin(domain, link)
    elif without_domain and not parsed_url.path.startswith("/"):
        return parse.urljoin(page_url, link)
    return link


def is_local(url, ref_url):
    url_domain = get_domain(url)
    ref_domain = get_domain(ref_url)
    if url_domain == ref_domain:
        return True
    return False


def make_file_path(link, directory):
    path, ext = os.path.splitext(link)
    if not ext:
        ext = ".html"
    file_name = make_name(path, ext)
    path = os.path.join(directory, file_name)
    _, tail = os.path.split(directory)
    rel_path = os.path.join(tail, file_name)
    return path, rel_path
