from pynng import Rep0
import trio
import click

async def reply(socket):
    while True:
        print('waiting for a message...')
        message = await socket.arecv()
        await socket.asend(b'hello back')

@click.command()
@click.argument('name')
def main(name):
    print(f'Started worker {name}')
    with Rep0(dial='tcp://127.0.0.1:54321') as socket:
        trio.run(reply, socket)

if __name__ == '__main__':
    main()
