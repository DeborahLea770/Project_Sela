import pytest

@pytest.fixture
def register_user():
    return {
      "email": "admin@sela.co.il",
      "password": "123456"
    }


@pytest.fixture
def unregister_user():
    return {
      "email": "deborahlea770@gmail.com",
      "password": "123456"
    }


def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="http://localhost")
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--packagename", action="store", default="C:/Users/debor/Downloads/chromedriver_win32/chromedriver.exe")


@pytest.fixture
def url(pytestconfig) -> str:
    """
    give the url from pytest options
    :param pytestconfig: pytestconfig fixture
    :return: url to integrate
    """
    return pytestconfig.getoption("url")

@pytest.fixture
def browser(pytestconfig) -> str:
    """
    give the browser from pytest options
    :param pytestconfig: pytestconfig fixture
    :return: browser to integrate
    """
    return pytestconfig.getoption("browser")


@pytest.fixture
def package_name(pytestconfig) -> str:
    """
    give the package_name from pytest options
    :param pytestconfig: pytestconfig fixture
    :return: package_name to integrate
    """
    return pytestconfig.getoption("packagename")

