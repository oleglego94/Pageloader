import pytest
from page_loader import resources

URL = "http://test.com"
DOMAIN = "http://test.com"


def test_get_domain():
    url = "http://test.com/projects/51/members/12473?step_id=219"
    assert resources.get_domain(url) == URL


@pytest.mark.parametrize(
    "link, page_url, result",
    [
        (
            "https://test.com/blog/about/photos/me.jpg",
            "https://site.com/blog/about",
            "https://test.com/blog/about/photos/me.jpg",
        ),
        (
            "//test.com/v3/",
            "https://test.com/v3/",
            "//test.com/v3/"
        ),
        (
            "/packs/runtime.js",
            "http://test.com/courses/",
            "http://test.com/packs/runtime.js",
        ),
        (
            "professions/nodejs/script.js",
            "http://test.com/courses/",
            "http://test.com/courses/professions/nodejs/script.js",
        ),
    ],
)
def test_normalize_link(link, page_url, result):
    assert resources.normalize_link(link, page_url) == result


@pytest.mark.parametrize(
    "url, domain, result",
    [
        ("https://cdn2.hexlet.io/assets/menu.css", DOMAIN, False),
        ("https://test.com/v3/", DOMAIN, False),
        ("http://test.com/packs/js/runtime.js", DOMAIN, True),
        ("http://test.com/professions/nodejs", DOMAIN, True),
    ],
)
def test_is_local(url, domain, result):
    assert resources.is_local(url, domain) == result


@pytest.mark.parametrize(
    "url, directory, path",
    [
        (
            "https://test.com/assets/menu.css",
            "test-com_files",
            "test-com_files/test-com-assets-menu.css",
        ),
        (
            "https://test.com/packs/js/runtime.js",
            "test-com_files",
            "test-com_files/test-com-packs-js-runtime.js",
        ),
        (
            "http://test.com/assets/professions/nodejs.png",
            "test-com_files",
            "test-com_files/test-com-assets-professions-nodejs.png",
        ),
    ],
)
def test_make_file_path(url, directory, path):
    _, rel_path = resources.make_file_path(url, directory)
    assert rel_path == path
