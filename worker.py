from pynng import Rep0
import trio
import click

async def reply(socket):
    for i in range(10):
        print('waiting for a message...')
        message = await socket.arecv()
        await socket.asend(b'hello back')

    print('Collecting messages')

@click.command()
@click.argument('name')
def main(name):
    print(f'Started worker {name}')
    with Rep0(dial='tcp://127.0.0.1:54321') as socket:
        while True:
            trio.run(reply, socket)

if __name__ == '__main__':
    main()
