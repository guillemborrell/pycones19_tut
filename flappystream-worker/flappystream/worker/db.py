import psycopg2
import click
from typing import Iterable


def a_create_table(database: str, user: str, password: str):
    with psycopg2.connect(f"dbname='{database}' user='{user}' host='localhost' password='{password}'") as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
        DROP TABLE IF EXISTS logs;
        CREATE TABLE IF NOT EXISTS logs (
            _id INTEGER,
            player VARCHAR,
            uuid VARCHAR(36),
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
            time_stamp BIGINT,
            score INTEGER ,
            best INTEGER 
            );
        """
        )


def insert_records(records: Iterable[tuple], conn: psycopg2.extensions.connection, table: str):
    cursor = conn.cursor()
    res = cursor.copy_from(table, records)
    conn.commit()
    return res


@click.command()
@click.option("--database", default="flappystream", help="Database name")
@click.option("--user", default="flappystream", help="Database account user name")
@click.option("--password", default="flappystream", help="Database account password")
def create_table(database, user, password):
    a_create_table(database, user, password)
