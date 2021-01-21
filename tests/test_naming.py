import pytest
from page_loader.naming import make_name


@pytest.mark.parametrize(
    "url, ext, result",
    [
        ("https://ru.hexlet.io/courses", ".html", "ru-hexlet-io-courses.html"),
        ("https://ru.hexlet.io/", "_files", "ru-hexlet-io_files"),
        ("https://ru.hexlet.io/js/runtime", ".js", "ru-hexlet-io-js-runtime.js"),  # noqa: E501
    ],
)
def test_make_name(url, ext, result):
    assert make_name(url, ext) == result
