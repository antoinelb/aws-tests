import os

import uvicorn
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.templating import Jinja2Templates

from . import api
from .logging import init_logging, logger


def create_app() -> Starlette:
    load_dotenv()
    init_logging()

    debug = os.environ.get("DEBUG", "0") == "1"
    app = Starlette(
        debug=debug  # type: ignore
    )
    app.templates = Jinja2Templates(  # type: ignore
        os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.environ.get("TEMPLATE_DIR", "templates"),
        )
    )
    app = api.add_routes(app)

    logger.debug("App created")

    return app


def run_server() -> None:
    init_logging()

    try:
        host = os.environ["HOST"]
        port = int(os.environ["PORT"])
    except KeyError:
        raise RuntimeError(
            "You need to set `HOST` and `PORT` environment variables."
        )

    reload = os.environ.get("RELOAD", "0") == "1"
    debug = os.environ.get("DEBUG", "0") == "1"
    log_level = "debug" if debug else "info"

    logger.info(f"Starting app in {'debug' if debug else 'production'} mode")

    uvicorn.run(
        "aws.app:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level,
        access_log=True,
    )


app = create_app()
