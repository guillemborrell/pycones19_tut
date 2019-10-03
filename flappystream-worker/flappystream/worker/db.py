import psycopg2
import click
import pandas as pd
import pickle
from io import StringIO


@click.command()
@click.option("--database", default="flappystream", help="Database name")
@click.option("--user", default="flappystream", help="Database account user name")
@click.option("--password", default="flappystream", help="Database account password")
@click.option(
    "--only", default="", help="Create only a particular table from [logs, models]"
)
def create_data_tables(database: str, user: str, password: str, only: str = ""):
    with psycopg2.connect(
        f"dbname='{database}' user='{user}' host='localhost' password='{password}'"
    ) as conn:
        cursor = conn.cursor()

        if not only or only == "logs":
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

        elif not only or only == "models":
            cursor.execute(
                f"""
                DROP TABLE IF EXISTS models;
                CREATE TABLE IF NOT EXISTS models (
                    updated timestamptz NOT NULL default NOW(),
                    name varchar(36),
                    pickle bytea
                );
                """
            )
        else:
            raise ValueError("Table name unknown")


def insert_dataframe(df: pd.DataFrame, conn: psycopg2.extensions.connection, table: str):
    """

    :param df:
    :param conn:
    :param table:
    :return:
    """
    cursor = conn.cursor()
    records = StringIO(df.to_csv(header=False, sep="\t", na_rep="\\N").replace("[", "{").replace("]", "}"))
    res = cursor.copy_from(table, records)
    conn.commit()
    return res


def load_model(model_name, conn):
    cursor = conn.cursor()
    cursor.execute(f"select pickle from models where name = '{model_name}' order by updated desc limit 1")
    data = cursor.fetchone()
    if data is None:
        return data
    else:
        return pickle.loads(data[0])


def dump_model(model, model_name, conn):
    cursor = conn.cursor()
    cursor.execute("insert into models (name, pickle) values (%s, %s)",
                   (model_name, psycopg2.Binary(pickle.dumps(model))))
    conn.commit()

