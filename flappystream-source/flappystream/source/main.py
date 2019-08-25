from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import Response
from pathlib import Path
import uvicorn
import click
import aiofiles
from pynng import Push0


# Stage 1


def build_app(backend_address="tcp://127.0.0.1", backend_port=54321):
    # Stage 1
    app = Starlette(debug=True)

    app.mount(
        "/static",
        app=StaticFiles(directory=Path(__file__).parent / "static"),
        name="static",
    )

    s = Push0(listen=f"{backend_address}:{backend_port}")

    # Stage 1
    @app.route("/")
    async def home(request):
        async with aiofiles.open(Path(__file__).parent / "static" / "index.html") as f:
            return Response(await f.read(), media_type="text/html")

    @app.websocket_route("/ws")
    async def ws1(ws):
        await ws.accept()
        print("Accepted websocket connection")
        while True:
            mess = await ws.receive()
            if "text" in mess:
                await s.asend(mess['text'].encode())

        await ws.close()

    return app


# Stage 1
@click.command()
@click.option("--host", default="0.0.0.0", help="hostname or IP")
@click.option("--port", default=8888, help="Port where the service is run")
@click.option("--backend_url", default="tcp://127.0.0.1", help="URL for the source socket")
def main(host="0.0.0.0", port=8888, backend_url="tcp://127.0.0.1:54321"):
    uvicorn.run(build_app(backend_url), host=host, port=port)
