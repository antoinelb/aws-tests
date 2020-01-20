import os

from aws.logging import init_logging


async def test_init_logging__dir_creation(mocker):
    path = os.path.join(
        os.path.dirname(__file__), os.pardir, os.pardir, "logs"
    )
    mocker.patch("aws.logging.os.path.exists", return_value=False)
    mkdir = mocker.patch("aws.logging.os.mkdir")
    init_logging()
    assert mkdir.calledOnceWith(path)
