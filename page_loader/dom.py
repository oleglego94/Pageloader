from bs4 import BeautifulSoup

from page_loader import storage, url

RESOURCES = {
    "img": "src",
    "link": "href",
    "script": "src",
}


def handle_html(html: str, page_url, dir_path):
    soup = BeautifulSoup(html, "html.parser")
    resources = get_local_resources(soup, page_url, dir_path)
    if resources:
        handled_html = soup.prettify(formatter="html5")
    else:
        handled_html = html
    return handled_html, resources


def get_local_resources(soup, page_url, dir_path) -> dict:
    local_resources = {}
    tags = soup.find_all(RESOURCES.keys())
    for tag in tags:
        attr = RESOURCES[tag.name]
        link = tag.get(attr)
        if not link or not url.is_local(link, page_url):
            continue
        normal_link = url.normalize_link(link, page_url)
        path, rel_path = storage.make_file_path(normal_link, dir_path)
        tag[attr] = rel_path
        local_resources[normal_link] = path
    return local_resources
