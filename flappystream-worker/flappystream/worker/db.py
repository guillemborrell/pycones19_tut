import triopg
import click
import trio_asyncio


async def a_create_table(database, user, password):
    connection_string = f"postgresql://{user}:{password}@localhost/{database}"
    async with triopg.connect(connection_string) as conn:
        await conn.execute(f"""
        DROP TABLE IF EXISTS logs;
        CREATE TABLE IF NOT EXISTS logs (
            _id SERIAL PRIMARY KEY,
            player VARCHAR,
            uuid VARCHAR(36) UNIQUE,
            alive BOOL,
            bird_x INTEGER,
            bird_y FLOAT,
            bird_radius INTEGER,
            bird_speed FLOAT ,
            bird_gravity FLOAT ,
            pipes_h INTEGER ,
            pipes_w INTEGER ,
            pipes_gap INTEGER ,
            pipes_position_x INTEGER[],
            pipes_position_y FLOAT[],
            frames INTEGER ,
            time_stamp INTEGER,
            score INTEGER ,
            best INTEGER 
            );
        """)

        await conn.close()

@click.command()
@click.option('--database', default='flappystream', help='Database name')
@click.option('--user', default='flappystream', help='Database account yser name')
@click.option('--password', default='flappystream', help='Database account password')
def create_table(database, user, password):
    trio_asyncio.run(a_create_table, database, user, password)