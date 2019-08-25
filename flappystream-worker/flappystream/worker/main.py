from pynng import Pull0, Pub0, Sub0
import click
import ujson
import trio
import numpy as np
from streamz import Stream
from operator import itemgetter
from flappystream.analysis import flatten_record


async def hub(socket, nursery_url):
    with Pub0(listen=nursery_url) as pub:
        while True:
            log = await socket.arecv()
            await pub.asend(log)


async def save_to_database(nursery_url):
    with Sub0(dial=nursery_url) as sub:
        sub.subscribe(b"")  # Subscribe to everything
        stream = Stream(asynchronous=False)
        stream.map(ujson.loads).map(flatten_record).partition(10).sink(print)
        while True:
            stream.emit(await sub.arecv())


async def average_bird_y(nursery_url):
    with Sub0(dial=nursery_url) as sub:
        sub.subscribe(b"")
        stream = Stream(asynchronous=False)
        stream.map(ujson.loads).map(flatten_record).map(
            itemgetter("bird_y")
        ).sliding_window(10).map(np.mean).sink(print)

        while True:
            stream.emit(await sub.arecv())


async def parent(socket, nursery_url):
    async with trio.open_nursery() as nursery:
        nursery.start_soon(hub, socket, nursery_url)
        nursery.start_soon(save_to_database, nursery_url)
        nursery.start_soon(average_bird_y, nursery_url)


@click.command()
@click.option(
    "--backend_url",
    default="tcp://127.0.0.1:54321",
    help="URL to dial for the source socket",
)
@click.option(
    "--nursery_url",
    default="tcp://127.0.0.1:54322",
    help="URL for the internal PUB-SUB queue",
)
def main(backend_url, nursery_url):
    print("Starting Flappystream worker")
    with Pull0(dial=backend_url) as socket:
        trio.run(parent, socket, nursery_url)
