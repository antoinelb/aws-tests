import os
import threading
import time

import pytest
import requests
from starlette.applications import Starlette

from aws.app import create_app, run_server


async def test_create_app(mocker):
    mocker.patch("aws.app.init_logging")
    mocker.patch("aws.app.logger")
    api = mocker.patch("aws.app.api")
    api.add_routes = lambda x: x

    app = create_app()
    assert isinstance(app, Starlette)


async def test_run():
    timeout = 1
    try_every = 0.1
    host = "127.0.0.1"
    port = 8001

    os.environ["HOST"] = host
    os.environ["PORT"] = str(port)
    os.environ["RELOAD"] = "0"
    os.environ["DEBUG"] = "0"

    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()

    time_ = 0
    while time_ < timeout:
        try:
            resp = requests.get(f"http://{host}:{port}/ping")
            assert resp.status_code == 200
            break
        except requests.exceptions.ConnectionError:
            time_ = time_ + try_every
            time.sleep(try_every)


async def test_run__missing_variables():
    host = "127.0.0.1"
    port = 8001

    del os.environ["HOST"]
    del os.environ["PORT"]

    with pytest.raises(RuntimeError):
        run_server()

    os.environ["HOST"] = host
    with pytest.raises(RuntimeError):
        run_server()
    del os.environ["HOST"]

    os.environ["PORT"] = str(port)
    with pytest.raises(RuntimeError):
        run_server()
