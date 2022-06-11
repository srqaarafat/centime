import pytest
import configparser
import os


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="test", help="select any env: test or prod"
    )


@pytest.fixture
def get_env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope='session')
def init_conf_prop():
    configs = configparser.ConfigParser()
    configs.read(os.path.join(os.getcwd(), 'config.properties'))
    return configs
