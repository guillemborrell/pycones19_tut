from pynng import Rep0
import trio
import click

async def reply(ntask, records=10):
    with Rep0(dial='tcp://127.0.0.1:54321') as socket:
        for i in range(records):
            print(f'Task {ntask} waiting for a message...')
            message = await socket.arecv()
            await socket.asend(b'hello back')

    print('Collecting messages')

async def parent(ntasks=4):
    async with trio.open_nursery() as nursery:
        for i in range(ntasks):
            nursery.start_soon(reply, i)
    
@click.command()
@click.argument('name')
def main(name):
    print(f'Started worker {name}')
    while True:
        trio.run(parent)

if __name__ == '__main__':
    main()
