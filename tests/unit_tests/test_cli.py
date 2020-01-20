import os
from unittest.mock import MagicMock

from aws.cli import cli, init_cli, run


async def test_cli(mocker, runner):
    init_logging = mocker.patch("aws.cli.init_logging")

    if "DEBUG" in os.environ:
        del os.environ["DEBUG"]

    resp = runner.invoke(cli)
    assert resp.exit_code == 0
    assert "Welcome to the aws api." in resp.output
    assert "Run aws --help for options." in resp.output
    init_logging.assert_called()
    assert os.environ.get("DEBUG", "0") == "0"

    resp = runner.invoke(cli, ["--debug"])
    assert resp.exit_code == 0
    init_logging.assert_called()
    assert os.environ.get("DEBUG", "0") == "1"

    resp = runner.invoke(cli, ["-h"])
    assert resp.exit_code == 0
    assert resp.output.startswith("Usage")


async def test_init_cli(mocker):
    command = MagicMock()
    mocker.patch("aws.cli.cli.command", return_value=command)
    run_server = mocker.patch("aws.cli.app.run_server")
    init_cli()
    command.assert_called_with(run_server)


async def test_run(mocker):
    init_cli = mocker.patch("aws.cli.init_cli")
    cli = mocker.patch("aws.cli.cli")
    run()
    init_cli.assert_called_once()
    cli.assert_called_once()
