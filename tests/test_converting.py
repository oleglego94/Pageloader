import pytest
from page_loader.downloading import convert_url


url = "https://ru.hexlet.io/courses"
result = "ru-hexlet-io-courses"

url1 = "https://ru.hexlet.io/"
result1 = "ru-hexlet-io"

url2 = "https://ru.hexlet.io/projects/51/members/12473?step_id=217"
result2 = "ru-hexlet-io-projects-51-members-12473-step_id-217"


@pytest.mark.parametrize(
    "url, result", [
        (url, result),
        (url1, result1),
        (url2, result2),
    ]
)
def test_convert(url, result):
    assert convert_url(url) == result
