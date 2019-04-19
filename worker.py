from pynng import Rep0
import trio
import click
import random
import json

async def reply(ntask, records=10):
    with Rep0(dial='tcp://127.0.0.1:54321') as socket:
        while True:
            for i in range(int(random.normalvariate(records, 4))):
                print(f'Task {ntask} waiting for a message...')
                message = await socket.arecv()
                parsed_message = json.loads(message)
                print(parsed_message)
                await socket.asend(b'hello back')

            print(f'Task {ntask} collecting messages')

async def parent(ntasks=4):
    async with trio.open_nursery() as nursery:
        for i in range(ntasks):
            nursery.start_soon(reply, i)


@click.command()
@click.argument('name')
def main(name):
    print(f'Started worker {name}')
    trio.run(parent)

if __name__ == '__main__':
    main()
