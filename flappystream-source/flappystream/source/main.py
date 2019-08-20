from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import Response
from pathlib import Path
import uvicorn
import click
import aiofiles

app = Starlette(debug=True)

app.mount(
    "/static",
    app=StaticFiles(directory=Path(__file__).parent / "static"),
    name="static",
)


@app.route("/")
async def home(request):
    async with aiofiles.open(Path(__file__).parent / "static" / "index.html") as f:
        return Response(await f.read(), media_type="text/html")


@click.command()
@click.option("--host", default="0.0.0.0", help="hostname or IP")
@click.option("--port", default=8888, help="Port where the service is run")
def main(host="0.0.0.0", port=8888):
    uvicorn.run(app, host=host, port=port)
