import os
from typing import Iterator

import pytest
from starlette.applications import Starlette
from starlette.templating import Jinja2Templates

from async_asgi_testclient import TestClient
from aws.app import create_app

from .config import *  # noqa


@pytest.yield_fixture
def app(init_config) -> Iterator[Starlette]:  # pylint: disable=unused-argument
    yield create_app()


@pytest.fixture
def client(app, event_loop) -> Iterator[TestClient]:
    yield TestClient(app)


@pytest.fixture
def other_client(other_app) -> TestClient:
    return TestClient(other_app)


@pytest.fixture
def templates() -> Jinja2Templates:
    return Jinja2Templates(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            os.environ.get("TEMPLATE_DIR", "templates"),
        )
    )
