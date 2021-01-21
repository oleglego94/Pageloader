import re


def make_name(url, extension):
    if url.endswith("/"):
        url = url[:-1]
    match = re.split(".*://", url)
    result = re.sub(r"\W", "-", match[1])
    return result + extension
