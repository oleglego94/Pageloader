import pytest

from page_loader import url

URL = "http://test.com"
ORIGIN = "http://test.com"


@pytest.mark.parametrize(
    "link, ext, file_name",
    [
        ("https://ru.hexlet.io/courses", ".html", "ru-hexlet-io-courses.html"),
        ("https://ru.hexlet.io/", "_files", "ru-hexlet-io_files"),
        (
            "https://ru.hexlet.io/js/runtime",
            ".js",
            "ru-hexlet-io-js-runtime.js",
        ),
    ],
)
def test_to_file_name(link, ext, file_name):
    assert url.to_file_name(link, ext) == file_name


@pytest.mark.parametrize(
    "resource_url, page_url, answer",
    [
        ("https://cdn2.hexlet.io/assets/menu.css", URL, False),
        ("//js.stripe.com/v3/", URL, False),
        ("/packs/js/runtime.js", URL, True),
        ("http://test.com/professions/nodejs", URL, True),
    ],
)
def test_is_local(resource_url, page_url, answer):
    assert url.is_local(resource_url, page_url) == answer


@pytest.mark.parametrize(
    "resource_url, page_url, result",
    [
        (
            "https://test.com/blog/about/photos/me.jpg",
            "https://site.com/blog/about",
            "https://test.com/blog/about/photos/me.jpg",
        ),
        ("//test.com/v3/", "https://test.com/v3/", "//test.com/v3/"),
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
def test_normalize_link(resource_url, page_url, result):
    assert url.normalize_link(resource_url, page_url) == result


@pytest.mark.parametrize(
    "link, result",
    [
        ("http://test.com/projects/51/members/12473?step_id=219", URL),
        ("//js.stripe.com/v3/", "://js.stripe.com"),
        ("/packs/js/runtime.js", ""),
        ("http:/professions/nodejs", "http://"),
    ],
)
def test_get_origin(link, result):
    assert url.get_origin(link) == result


@pytest.mark.parametrize(
    "link, dir_path, path, rel_path",
    [
        (
            "https://test.com/assets/menu.css",
            "../app/test-com_files",
            "../app/test-com_files/test-com-assets-menu.css",
            "test-com_files/test-com-assets-menu.css",
        ),
        (
            "https://test.com/packs/js/runtime.js",
            "./app/page-loader/test-com_files",
            "./app/page-loader/test-com_files/test-com-packs-js-runtime.js",
            "test-com_files/test-com-packs-js-runtime.js",
        ),
        (
            "http://test.com/assets/professions/nodejs.png",
            "test-com_files",
            "test-com_files/test-com-assets-professions-nodejs.png",
            "test-com_files/test-com-assets-professions-nodejs.png",
        ),
    ],
)
def test_make_file_path(link, dir_path, path, rel_path):
    assert url.make_file_path(link, dir_path) == (path, rel_path)
