from pynng import Rep0
import pandas as pd
import trio
import click
import random
import ujson
import io
import sys
from uuid import uuid4
from pathlib import Path

async def save_chunk(chunk: pd.DataFrame):
    buf = io.BytesIO()
    chunk.to_parquet(buf)
    await trio.Path(str(uuid4()) + '.parquet').write_bytes(buf.getvalue())
        

async def reply(ntask: int, nrecords: int=10, ncycles=sys.maxsize):
    with Rep0(dial='tcp://127.0.0.1:54321') as socket:
        for j in range(ncycles):
            records = []
            for i in range(int(random.normalvariate(nrecords, 4))):
                message = await socket.arecv()
                records.append(ujson.loads(message))
                await socket.asend(b'Response')

            print(f'Task {ntask} collecting messages')
            await save_chunk(pd.DataFrame(records)
                               .assign(when=lambda df:pd.to_datetime(df.when))
            )
        

async def parent(ntasks: int=4):
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
