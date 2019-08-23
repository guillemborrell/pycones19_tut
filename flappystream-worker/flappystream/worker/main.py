from pynng import Pull0
import click
import trio


async def worker(socket):
    try:
        while True:
            print(await socket.arecv())
    except KeyboardInterrupt:
        print("Cleaning up")


@click.command()
@click.option('--backend_address', default="tcp://127.0.0.1", help="Address to dial for the source socket")
@click.option('--backend_port', default=54321, help="Port fo the source socket")
def main(backend_address, backend_port):
    with Pull0(dial=f"{backend_address}:{backend_port}") as socket:
        trio.run(worker, socket)
