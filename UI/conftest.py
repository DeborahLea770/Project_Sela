import pytest


def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="http://localhost")
    parser.addoption("--chromeDriver", action="store", default="C:/Users/debor/Downloads/chromedriver_win32/chromedriver.exe")


@pytest.fixture
def url(pytestconfig) -> str:
    """
    give the url from pytest options
    :param pytestconfig: pytestconfig fixture
    :return: url to integrate
    """
    return pytestconfig.getoption("url")


@pytest.fixture
def chromeDriver(pytestconfig) -> str:
    """
    give the chromedriver from pytest options
    :param pytestconfig: pytestconfig fixture
    :return: url to integrate
    """
    return pytestconfig.getoption("chromeDriver")

