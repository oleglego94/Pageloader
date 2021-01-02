import pytest
from page_loader import convert


url = "https://ru.hexlet.io/courses"
result = "ru-hexlet-io-courses.html"

url1 = "https://ru.hexlet.io/"
result1 = "ru-hexlet-io.html"

url2 = "https://ru.hexlet.io/projects/51/members/12473?step_id=217"
result2 = "ru-hexlet-io-projects-51-members-12473-step_id-217.html"


@pytest.mark.parametrize(
    "url, result", [(url, result), (url1, result1), (url2, result2)]
)
def test_convert(url, result):
    assert convert(url) == result
