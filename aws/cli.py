import os

import click

from . import app
from .logging import init_logging


@click.group(
    invoke_without_command=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.option(
    "--debug", default=False, is_flag=True, help="Show debug messages."
)
@click.pass_context
def cli(ctx, debug: bool = False) -> None:
    if ctx.invoked_subcommand is None:
        click.echo("Welcome to the aws api.")
        click.echo("Run aws --help for options.")
    if debug:
        os.environ["DEBUG"] = "1"
    init_logging()


def init_cli() -> None:
    cli.command(short_help="Run the server")(app.run_server)
    cli.command("r", hidden=True)(app.run_server)


def run() -> None:
    init_cli()
    cli()  # pylint: disable=no-value-for-parameter
