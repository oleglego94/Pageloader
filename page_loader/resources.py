import logging
import os
from bs4 import BeautifulSoup
from urllib import parse
from page_loader.saving import save
from page_loader.naming import make_name
from page_loader.logging import setup_logging

RESOURCES = {
    "img": "src",
    "link": "href",
    "script": "src",
}

setup_logging()


def get_local_resources(html_path, directory, url):
    domain = get_domain(url)
    soup = make_soup(html_path)
    for resource in RESOURCES.keys():
        tags = soup.find_all(resource)
        attr = RESOURCES[resource]
        get_resource(tags, attr, domain, directory)

    return soup.prettify(formatter="html5")


def get_resource(tags, attr, domain, directory):
    for tag in tags:
        link = tag.get(attr)
        normal_link = normalize_link(link, domain)
        if not is_local(normal_link, domain):
            continue
        else:
            path, rel_path = make_file_path(normal_link, directory)
            save(normal_link, path)
            logging.info(f"{normal_link} was successfully downloaded into '{rel_path}'")  # noqa: E501
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


def normalize_link(url, domain):
    parsed_url = parse.urlparse(url)
    if not parsed_url.scheme and not parsed_url.netloc:
        return parse.urljoin(domain, url)
    return url


def is_local(url, ref_domain):
    url_domain = get_domain(url)
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
