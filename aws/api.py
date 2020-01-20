from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response


def add_routes(app: Starlette) -> Starlette:
    app.add_route("/ping", ping, name="ping", methods=["GET", "POST"])
    return app


async def ping(_: Request) -> Response:
    return PlainTextResponse("Pong!")
