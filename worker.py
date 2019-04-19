from pynng import Rep0
import pandas as pd
import trio
import click
import random
import json

async def reply(ntask, nrecords=10):
    with Rep0(dial='tcp://127.0.0.1:54321') as socket:
        while True:
            records = []
            for i in range(int(random.normalvariate(nrecords, 4))):
                message = await socket.arecv()
                records.append(json.loads(message))
                await socket.asend(b'Response')

            print(f'Task {ntask} collecting messages')
            df = (pd.DataFrame(records)
                    .assign(when=lambda df:pd.to_datetime(df.when))
                  )
            print(df.head())

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
