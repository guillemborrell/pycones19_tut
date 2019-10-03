from flappystream.analysis import (
    flatten_record,
    build_game_independent_vars,
    build_game_dependent_vars,
    build_multiple_games_table,
    build_game_table,
    train_test,
    model_test,
    model_train
)
from pathlib import Path
import json
import pandas as pd
from sklearn.linear_model import SGDClassifier
from streamz import Stream
from functools import partial


def test_data_dir():
    return Path(__file__).parent / "data"


def test_flatten_record():
    result = flatten_record(json.loads(open(test_data_dir() / "logs.dat").readline()))
    assert isinstance(result, dict)
    assert len(result) == 17


def test_build_game_independent_vars():
    df = pd.read_parquet(test_data_dir() / "logs.parq")
    df1 = df.groupby("uuid").get_group(df.uuid.unique()[0])
    X = build_game_independent_vars(df1)
    assert len(X) == 20
    assert len(X.columns) == 5


def test_build_game_dependent_vars():
    df = pd.read_parquet(test_data_dir() / "logs.parq")
    df1 = df.groupby("uuid").get_group(df.uuid.unique()[0])
    Y = build_game_dependent_vars(df1)

    assert len(Y) == 20
    assert len(Y.columns) == 1


def check_train_size():
    df = pd.read_parquet(test_data_dir() / "logs.parq")
    df1 = df.groupby("uuid").get_group(df.uuid.unique()[0])
    X = build_game_independent_vars(df1)
    Y = build_game_dependent_vars(df1)

    assert len(X) == len(Y)


def test_build_game_independent_vars_hard():
    df = pd.read_parquet(test_data_dir() / "logs.parq")
    df1 = df.groupby("uuid").get_group("bf98beac-451c-4386-825f-46b63da17de7")
    X = build_game_independent_vars(df1)
    assert len(X) == 111
    assert len(X.columns) == 5


def test_build_game_dependent_vars_hard():
    df = pd.read_parquet(test_data_dir() / "logs.parq")
    df1 = df.groupby("uuid").get_group("bf98beac-451c-4386-825f-46b63da17de7")
    Y = build_game_dependent_vars(df1)

    print(
        df1[["pipes_position_x", "alive"]]
        .explode("pipes_position_x")
        .assign(flap=lambda df2: df2.index)
        .reset_index()
    )
    assert len(Y) == 111
    assert len(Y.columns) == 1


def test_build_game_table():
    df = pd.read_parquet(test_data_dir() / "logs.parq")
    df1 = df.groupby("uuid").get_group(df.uuid.unique()[0])
    X = build_game_table(df1)

    assert len(X.columns) == 6


def test_build_multiple_game_tables():
    df = pd.read_parquet(test_data_dir() / "logs.parq")
    X = build_multiple_games_table(df)

    assert len(X) == 986
    assert len(X.columns) == 6


def test_train_test():
    df = pd.read_parquet(test_data_dir() / "logs.parq")
    X = build_multiple_games_table(df)

    assert train_test(X) > 0.01


def test_successive_train_test():
    df = pd.read_parquet(test_data_dir() / "logs.parq")
    model = SGDClassifier()
    source = Stream()
    result = (source
        .map(build_game_table)
        .map(partial(model_train, model, None))
        .map(partial(model_test, model, None))
        .sink_to_list())

    for g, d in df.groupby("uuid"):
        source.emit(d)

    assert len(result) == 24


def test_successive_train_test_db(postgresql_db):
    with postgresql_db.engine.connect() as connection:
        conn = connection.connection
        cursor = conn.cursor()

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

        df = pd.read_parquet(test_data_dir() / "logs.parq")

        source = Stream()
        result = (source
                  .map(build_game_table)
                  .map(partial(model_train, None, conn))
                  .map(partial(model_test, None, conn))
                  .sink_to_list())

        for g, d in df.groupby("uuid"):
            source.emit(d)

        conn.commit()
        assert len(result) == 24


