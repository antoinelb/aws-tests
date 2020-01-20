import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def init_config():
    os.environ["DEBUG"] = "1"
    os.environ["HOST"] = "127.0.0.1"
    os.environ["PORT"] = "8001"
    os.environ["RELOAD"] = "0"
