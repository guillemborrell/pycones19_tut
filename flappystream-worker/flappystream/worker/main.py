from pynng import Pub0, Sub0
import click
import ujson
import trio
import pandas as pd
import psycopg2
from streamz import Stream
from flappystream.analysis import flatten_record, model_train, model_test, build_game_table
from flappystream.worker.db import insert_dataframe
from functools import partial


async def hub(socket, nursery_url):
    with Pub0(listen=nursery_url) as pub:
        while True:
            log = await socket.arecv()
            await pub.asend(log)


async def save_to_database(nursery_url, conn, partition_size=100):
    with Sub0(dial=nursery_url) as sub:
        sub.subscribe(b"")  # Subscribe to everything

        stream = Stream(asynchronous=False)

        (
            stream.map(ujson.loads)
            .flatten()
            .map(flatten_record)
            .partition(partition_size)
            .map(pd.DataFrame)
            .sink(partial(insert_dataframe, "logs", conn))
        )

        while True:
            stream.emit(await sub.arecv())


async def model_flap(nursery_url, conn, partition_size=100):
    with Sub0(dial=nursery_url) as sub:
        sub.subscribe(b"")

        stream = Stream(asynchronous=False)

        (
            stream.map(ujson.loads)
            .flatten()
            .map(flatten_record)
            .partition(partition_size)
            .map(pd.DataFrame)
            .map(build_game_table)
            .map(partial(model_train, None, conn))
            .map(partial(model_test, None, conn))
            .sink(print)
        )

        while True:
            stream.emit(await sub.arecv())


async def parent(socket, connection_string, nursery_url):
    with psycopg2.connect(connection_string) as conn:
        async with trio.open_nursery() as nursery:
            nursery.start_soon(hub, socket, nursery_url)
            nursery.start_soon(save_to_database, nursery_url, conn)
            nursery.start_soon(model_flap, nursery_url, conn)


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

    with Sub0(dial=backend_url) as socket:
        socket.subscribe(b"") #  Subscribe to everything
        trio.run(parent, socket, connection_string, nursery_url)
