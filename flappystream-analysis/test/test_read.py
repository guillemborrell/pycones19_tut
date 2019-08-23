from flappystream.analysis import read_logs, flatten_record, read_log_file, a_read_log_file
from pathlib import Path
import pandas as pd
import json
import pytest


def test_data_dir():
    return Path(__file__).parent / 'data'


def test_flatten_record():
    result = flatten_record(json.loads(open(test_data_dir() / 'logs.dat').readline()))
    assert isinstance(result, dict)
    assert len(result) == 16


def test_read_logs():
    result = read_logs(open(test_data_dir() / 'logs.dat').readlines())
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 49


def test_read_log_file():
    result = list(read_log_file(test_data_dir() / 'logs.dat'))
    assert isinstance(result, list)
    assert len(result) == 17


@pytest.mark.asyncio
async def test_a_read_logs():
    result = list(await a_read_log_file(test_data_dir() / 'logs.dat'))
    assert isinstance(result, list)
    assert len(result) == 17
