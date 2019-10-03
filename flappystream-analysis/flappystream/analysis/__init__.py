import pandas as pd
import numpy as np
from sklearn import metrics, model_selection, linear_model
from typing import Tuple


def flatten_record(record: dict) -> dict:
    """
    Transforms the nested dict obtained from the data record to a flat dict, more suitable for storage

    :param record: (dict) Record from the data source
    :return: (dict) Flattened record
    """
    return {
        "player": record["player"] if record["player"] else np.nan,
        "uuid": record["uuid"],
        "alive": record["alive"],
        "bird_x": record["bird"]["x"],
        "bird_y": record["bird"]["y"],
        "bird_radius": record["bird"]["radius"],
        "bird_speed": record["bird"]["speed"],
        "bird_gravity": record["bird"]["gravity"],
        "pipes_h": record["pipes"]["h"],
        "pipes_w": record["pipes"]["w"],
        "pipes_gap": record["pipes"]["gap"],
        "pipes_position_x": [
            p["x"] for p in record["pipes"]["position"] if record["pipes"]["position"]
        ],
        "pipes_position_y": [
            p["y"] for p in record["pipes"]["position"] if record["pipes"]["position"]
        ],
        "frames": record["frames"],
        "timestamp": record["timestamp"],
        "score": record["score"]["value"],
        "best": record["score"]["best"],
    }


def build_game_independent_vars(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df:
    :return:
    """
    return (
        df[
            [
                "bird_x",
                "bird_y",
                "bird_speed",
                "pipes_position_x",
                "pipes_position_y",
                "alive",
            ]
        ]
        .explode("pipes_position_x")
        .assign(
            pipes_position_y=lambda df1: df1.assign(idx=lambda df2: df2.index)
            .drop_duplicates(subset="idx", keep="first")
            .explode("pipes_position_y")
            .pipes_position_y
        )
        .astype({"pipes_position_x": float, "pipes_position_y": float})
        .eval("pipes_position_y = bird_y + pipes_position_y")
        .eval("pipes_position_x = pipes_position_x - bird_x")
        .assign(flap=lambda df1: df1.index)
        .assign(pipe=lambda df1: df1.groupby("flap").cumcount())
        .query("alive == True")
        .drop(columns=["flap", "bird_x", "alive"])
    )


def build_game_dependent_vars(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df:
    :return:
    """

    base = (
        df[["pipes_position_x", "alive"]]
        .explode("pipes_position_x")
        .assign(flap=lambda df1: df1.index)
        .reset_index()
    )

    if base.alive.values.all():
        return base[["alive"]]

    else:
        changes = (
            base[lambda df2: ~df2.alive]
            .assign(new_index=lambda df2: df2.index - len(df2))
            .set_index("new_index")
            .assign(alive=False)
        )

        base.update(changes)
        return base.iloc[: -len(changes)][["alive"]]


def build_game_table(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df:
    :return:
    """
    X = build_game_independent_vars(df)
    Y = build_game_dependent_vars(df)

    return X.assign(successful=Y.alive.values)


def build_multiple_games_table(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df:
    :return:
    """
    return pd.concat(
        (build_game_table(df1) for g, df1 in df.groupby("uuid")), ignore_index=True
    )


def balance_successful(x_train: np.array, y_train: np.array) -> Tuple[np.array, np.array]:
    """

    :param x_train:
    :param y_train:
    :return:
    """
    successful_mask = y_train.astype(np.bool)
    indices = np.arange(y_train.shape[0])[successful_mask]

    x_train_unsuccessful = x_train[~successful_mask]
    y_train_unsuccessful = y_train[~successful_mask]

    n_unsuccessful = 2*(y_train.shape[0] - y_train.sum())

    successful_choices = np.random.choice(indices, n_unsuccessful)

    x_train = np.vstack((x_train_unsuccessful, x_train[successful_choices]))
    y_train = np.hstack((y_train_unsuccessful, y_train[successful_choices]))

    return x_train, y_train


def wrangle_train_data(data: pd.DataFrame) -> Tuple[np.array, np.array]:
    data = data.dropna()
    x = data.iloc[:, :5].values
    y = data.iloc[:, 5].values.astype(np.int)

    return balance_successful(x, y)


def wrangle_test_data(data: pd.DataFrame) -> Tuple[np.array, np.array]:
    data = data.dropna()
    x = data.iloc[:, :5].values
    y = data.iloc[:, 5].values.astype(np.int)

    return x, y


def train_test(data: pd.DataFrame) -> float:
    """

    :param data:
    :return:
    """
    data = data.dropna()

    x = data.iloc[:, :5].values
    y = data.iloc[:, 5].values.astype(np.int)

    x_train, x_test, y_train, y_test = model_selection.train_test_split(
        x, y, test_size=0.3
    )

    # Balance between the two classes
    x_train, y_train = balance_successful(x_train, y_train)

    prediction = linear_model.SGDClassifier().fit(x_train, y_train).predict(x_test)

    return metrics.accuracy_score(prediction, y_test)


def train(model, data: pd.DataFrame):
    if len(data) > 10:  # Train with enough data
        x_train, y_train = wrangle_train_data(data)
        try:
            model.partial_fit(x_train, y_train, classes=np.unique(y_train))
        except ValueError:
            print('Set with unsuccessful flaps')

    return data


def accuracy(model, data: pd.DataFrame):
    if len(data) > 10:  # Test with enough data
        # TODO: try to get the model from DB
        x_test, y_test = wrangle_test_data(data)
        prediction = model.predict(x_test)
        return metrics.accuracy_score(prediction, y_test)

    else:
        return 0



