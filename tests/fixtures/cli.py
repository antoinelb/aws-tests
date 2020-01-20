import click.testing
import pytest

from aws.cli import init_cli


@pytest.fixture(scope="session")
def runner():
    init_cli()
    return click.testing.CliRunner()
