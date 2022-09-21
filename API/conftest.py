import pytest

def pytest_addoption(parser):
        parser.addoption("--url", action="store", default="http://localhost")

@pytest.fixture
def url_config(request):
        url = request.config.getoption("url")
        return url


