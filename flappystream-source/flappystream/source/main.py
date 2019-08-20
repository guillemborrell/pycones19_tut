from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import Response
from pathlib import Path
import uvicorn
import click
import aiofiles


# Stage 1
def process_log(log):
    print(log)


def build_app():
    # Stage 1
    app = Starlette(debug=True)

    app.mount(
        "/static",
        app=StaticFiles(directory=Path(__file__).parent / "static"),
        name="static",
    )

    # Stage 1
    @app.route("/")
    async def home(request):
        async with aiofiles.open(Path(__file__).parent / "static" / "index.html") as f:
            return Response(await f.read(), media_type="text/html")

    # Stage 1
    @app.route("/log", methods=['POST'])
    async def log(request):
        process_log(await request.body())
        return Response("")

    return app


# Stage 1
@click.command()
@click.option("--host", default="0.0.0.0", help="hostname or IP")
@click.option("--port", default=8888, help="Port where the service is run")
def main(host="0.0.0.0", port=8888):
    uvicorn.run(build_app(), host=host, port=port)
