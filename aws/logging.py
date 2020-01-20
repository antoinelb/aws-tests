import logging
import logging.config
import os
import sys

import click

logger = logging.getLogger("aws-tests")


def init_logging() -> None:
    "Configures the logger."

    debug = os.environ.get("DEBUG", "0") == "1"

    if not os.path.exists(
        os.path.join(os.path.dirname(__file__), os.pardir, "logs")
    ):
        os.mkdir(os.path.join(os.path.dirname(__file__), os.pardir, "logs"))

    config = {
        "disable_existing_loggers": True,
        "formatters": {
            "simple": {
                "format": "%(levelname)s - %(message)s",
                "class": "aws.logging.ColourFormatter",
            },
            "complete": {
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": "%(asctime)s - "
                "%(name)s - "
                "%(levelname)s - "
                "%(message)s",
            },
        },
        "filters": {"ping": {"()": PingFilter}},
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
                "level": "DEBUG" if debug else "INFO",
                #  "filters": ["ping"],
            },
            "file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "complete",
                "filename": os.path.join(
                    os.path.dirname(__file__), os.pardir, "logs", "log"
                ),
                "level": "DEBUG" if debug else "INFO",
                "when": "midnight",
                #  "filters": ["ping"],
            },
        },
        "loggers": {
            "aws-tests": {
                "handlers": ["console", "file"],
                "level": "DEBUG" if debug else "INFO",
                "propagate": True,
            },
            "databases": {
                "handlers": ["console", "file"],
                "level": "DEBUG" if debug else "INFO",
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": "DEBUG" if debug else "INFO",
                "propagate": False,
            },
        },
        "version": 1,
    }
    logging.config.dictConfig(config)


class ColourFormatter(logging.Formatter):
    level_name_colours = {
        logging.DEBUG: lambda level: click.style(str(level), fg="cyan"),
        logging.INFO: lambda level: click.style(str(level), fg="green"),
        logging.WARNING: lambda level: click.style(str(level), fg="yellow"),
        logging.ERROR: lambda level: click.style(str(level), fg="red"),
        logging.CRITICAL: lambda level: click.style(
            str(level), fg="bright_red"
        ),
    }

    def __init__(self, fmt=None, datefmt=None, style="%", use_colours=None):
        if use_colours in (True, False):
            self.use_colours = use_colours  # pragma: no cover
        else:
            self.use_colours = sys.stdout.isatty()
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def colour_level_name(self, level_name, level_no):
        fct = self.level_name_colours.get(
            level_no,
            lambda level_name: str(  # pylint: disable=unnecessary-lambda
                level_name
            ),
        )  # pragma: no cover
        return fct(level_name)  # pragma: no cover

    def formatMessage(self, record):
        if self.use_colours:
            record.levelname = self.colour_level_name(
                record.levelname, record.levelno
            )  # pragma: no cover
        return super().formatMessage(record)


class PingFilter(logging.Filter):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def filter(self, record) -> bool:
        return not record.getMessage().endswith('"GET /ping HTTP/1.1" 200')
