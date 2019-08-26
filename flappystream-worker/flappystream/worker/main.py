from pynng import Pull0, Pub0, Sub0
import click
import ujson
import trio
import numpy as np
import pandas as pd
import psycopg2
from io import StringIO
from streamz import Stream
from operator import itemgetter, methodcaller
from flappystream.analysis import flatten_record
from flappystream.worker.db import insert_records
from functools import partial


async def hub(socket, nursery_url):
    with Pub0(listen=nursery_url) as pub:
        while True:
            log = await socket.arecv()
            await pub.asend(log)


async def save_to_database(nursery_url, conn):
    with Sub0(dial=nursery_url) as sub:
        sub.subscribe(b"")  # Subscribe to everything

        stream = Stream(asynchronous=False)

        (
            stream.map(ujson.loads)
            .flatten()
            .map(flatten_record)
            .partition(10)
            .map(pd.DataFrame)
            .map(methodcaller("to_csv", header=False, sep="\t", na_rep="\\N"))
            .map(methodcaller("replace", "[", "{"))
            .map(methodcaller("replace", "]", "}"))
            .map(StringIO)
            .sink(partial(insert_records, "logs", conn))
        )

        while True:
            stream.emit(await sub.arecv())


async def average_bird_y(nursery_url):
    with Sub0(dial=nursery_url) as sub:
        sub.subscribe(b"")

        stream = Stream(asynchronous=False)

        stream.map(ujson.loads).flatten().map(flatten_record).map(
            itemgetter("bird_y")
        ).sliding_window(10).map(np.mean).sink(print)

        while True:
            stream.emit(await sub.arecv())


async def parent(socket, connection_string, nursery_url):
    with psycopg2.connect(connection_string) as conn:
        async with trio.open_nursery() as nursery:
            nursery.start_soon(hub, socket, nursery_url)
            nursery.start_soon(save_to_database, nursery_url, conn)
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
@click.option("--database", default="flappystream", help="Database name")
@click.option("--user", default="flappystream", help="Database account user name")
@click.option("--password", default="flappystream", help="Database account password")
def main(backend_url, nursery_url, database, user, password):
    print("Starting flappybird worker")
    connection_string = (
        f"dbname='{database}' user='{user}' host='localhost' password='{password}'"
    )

    with Pull0(dial=backend_url) as socket:
        trio.run(parent, socket, connection_string, nursery_url)
