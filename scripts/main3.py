from pynng import Sub0, Pub0
from streamz import Stream
import ujson
import trio
from flappystream.analysis import flatten_record


async def parent(socket):
    async with trio.open_nursery() as nursery:
        nursery.start_soon(hub, socket)
        nursery.start_soon(worker1)
        nursery.start_soon(worker2)


async def hub(socket):
    with Pub0(listen="tcp://127.0.0.1:54322") as pub:
        while True:
            await pub.asend(await socket.arecv())


async def worker1():
    with Sub0(dial="tcp://127.0.0.1:54322") as sub:
        sub.subscribe(b"")

        print('worker1', len(await sub.arecv()))


async def worker2():
    with Sub0(dial="tcp://127.0.0.1:54322") as sub:
        sub.subscribe(b"")

        print("worker2", len(await sub.arecv()))


if __name__ == "__main__":
    with Sub0(dial="tcp://127.0.0.1:54321") as socket:
        print('Connecting...')
        socket.subscribe(b"")
        trio.run(parent, socket)