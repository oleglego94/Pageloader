from bs4 import BeautifulSoup

from page_loader import url

RESOURCES = {
    "img": "src",
    "link": "href",
    "script": "src",
}


def prepare_html(html: str, page_url, dir_path):
    soup = BeautifulSoup(html, "html.parser")
    local_resources = {}
    tags = soup.find_all(RESOURCES.keys())

    for tag in tags:
        attr = RESOURCES[tag.name]
        link = tag.get(attr)
        if not link or not url.is_local(link, page_url):
            continue
        normal_link = url.normalize_link(link, page_url)
        path, rel_path = url.make_file_path(normal_link, dir_path)
        tag[attr] = rel_path
        local_resources[normal_link] = path

    if local_resources:
        return soup.prettify(formatter="html5"), local_resources
    else:
        return html, local_resources
