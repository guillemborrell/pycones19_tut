import triopg
import click
import trio_asyncio


async def a_create_table(database, user, password):
    connection_string = f"postgresql://{user}:{password}@localhost/{database}"
    print('++++++++', connection_string)
    async with triopg.connect(connection_string) as conn:
        await conn.execute(f"""
        DROP TABLE IF EXISTS logs;
        CREATE TABLE IF NOT EXISTS logs (
            _id SERIAL PRIMARY KEY,
            uuid VARCHAR(36) UNIQUE
            );
        """)

        await conn.close()

@click.command()
@click.option('--database', default='flappystrean', help='Database name')
@click.option('--user', default='flappystream', help='Database account yser name')
@click.option('--password', default='flappystream', help='Database account password')
def create_table(database, user, password):
    trio_asyncio.run(a_create_table, database, user, password)