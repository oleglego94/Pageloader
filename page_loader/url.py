import re
from urllib import parse


def to_file_name(url, extension):
    if url.endswith("/"):
        url = url[:-1]
    match = re.split(".*://", url)
    result = re.sub(r"\W", "-", match[1])
    return result + extension


def to_dir_name(url):
    dir_name = to_file_name(url, "_files")
    return dir_name


def is_local(resource_url, page_url):
    resource_origin = get_origin(resource_url)
    page_origin = get_origin(page_url)
    if not resource_origin:
        return True
    elif resource_origin == page_origin:
        return True
    else:
        return False


def normalize_link(resource_url, page_url):
    resource_origin = get_origin(resource_url)
    page_origin = get_origin(page_url)
    if not resource_origin and resource_url.startswith("/"):
        return parse.urljoin(page_origin, resource_url)
    elif not resource_origin and not resource_url.startswith("/"):
        return parse.urljoin(page_url, resource_url)
    return resource_url


def get_origin(url):
    parsed_url = parse.urlparse(url)
    scheme = parsed_url.scheme
    host = parsed_url.netloc
    if not scheme and not host:
        return ""
    return f"{scheme}://{host}"
