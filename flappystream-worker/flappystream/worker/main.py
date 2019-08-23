from pynng import Pull0, Pub0, Sub0
import click
import trio


async def hub(socket, nursery_port):
    with Pub0(listen=f"tcp://127.0.0.1:{nursery_port}") as pub:
        while True:
            log = await socket.arecv()
            await pub.asend(log)


async def echo(nursery_port):
    with Sub0(dial=f"tcp://127.0.0.1:{nursery_port}") as sub:
        sub.subscribe(b"")  # Subscribe to everything
        while True:
            log = await sub.arecv()


async def parent(socket, nursery_port):
    async with trio.open_nursery() as nursery:
        nursery.start_soon(echo, nursery_port)
        nursery.start_soon(hub, socket, nursery_port)


@click.command()
@click.option(
    "--backend_address",
    default="tcp://127.0.0.1",
    help="Address to dial for the source socket",
)
@click.option("--backend_port", default=54321, help="Port fo the source socket")
@click.option(
    "--nursery_port",
    default=54322,
    help="Port to be used to broadcast the message to all the workers",
)
def main(backend_address, backend_port, nursery_port):
    with Pull0(dial=f"{backend_address}:{backend_port}") as socket:
        trio.run(parent, socket, nursery_port)
