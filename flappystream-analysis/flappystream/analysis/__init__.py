import pandas as pd
import numpy as np
import ujson
import aiofiles
from pathlib import Path
from typing import Iterable, Union


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


def read_logs(logs: Iterable[str]) -> pd.DataFrame:
    """

    :param logs:
    :return:
    """
    records = pd.DataFrame(flatten_record(ujson.loads(record)) for record in logs)
    return (
        records.merge(
            pd.concat(
                [
                    records.pipes_position_x.explode(),
                    records.pipes_position_y.explode(),
                ],
                axis=1,
            ),
            left_index=True,
            right_index=True,
        )
        .assign(flap=lambda df: df.index.values)
        .drop(columns=["pipes_position_x_x", "pipes_position_y_x"])
        .rename(
            columns={
                "pipes_position_x_y": "pipes_position_x",
                "pipes_position_y_y": "pipes_position_y",
            }
        )
        .assign(pipes_position_x=lambda df: df.pipes_position_x.astype(np.float))
        .assign(pipes_position_y=lambda df: df.pipes_position_y.astype(np.float))
        .assign(bird_x=lambda df: df.bird_x.astype(np.float64))
        .assign(pipes_h=lambda df: df.pipes_h.astype(np.float64))
        .eval("pipes_position_y = pipes_position_y + pipes_h")
    )


def read_log_file(f: Union[Path, str]) -> pd.DataFrame:
    """
    Reads a file containing data record and returns an iterable with the records as dicts

    :param f:
    :return:
    """
    return read_logs(Path(f).open())


async def a_read_log_file(f: Union[Path, str]) -> Iterable[dict]:
    """

    :param f:
    :return:
    """
    async with aiofiles.open(Path(f).resolve()) as f:
        return read_logs(await f.readlines())
