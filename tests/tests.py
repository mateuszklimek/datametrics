import pdb

from datametrics import transform
from datametrics.settings import (
    CRYPTO_TO_TRACK,
    CRYPTO_EXPORTED_METRICS,
    STOCKS_TO_TRACK,
    STOCKS_EXPORTED_METRICS,
)
import json


def has_all_metrics(el):
    return all(metric in el for metric in ["name", "value", "interval", "time"])


def get_json_from_file(file_path):
    with open(file_path) as f:
        data = json.load(f)

    return data


def test_parsing_livecoin():

    data = get_json_from_file("tests/tests_data/sample_livecoin.json")

    metrics = transform.livecoin_to_metrics(data)

    assert len(metrics) == len(CRYPTO_TO_TRACK) * len(CRYPTO_EXPORTED_METRICS)
    assert all(has_all_metrics(el) for el in metrics)

    metric_names = [m["name"] for m in metrics]
    some_expected_symbols = [
        "crypto.BTC/USD-last",
        "crypto.BTC/USD-low",
        "crypto.ETH/USD-last",
    ]

    assert all(symbol in metric_names for symbol in some_expected_symbols)

    print(metrics)


def test_parsing_iex():

    data = get_json_from_file("tests/tests_data/sample_iex.json")

    metrics = transform.iex_to_metrics(data)

    assert len(metrics) == len(STOCKS_TO_TRACK) * len(STOCKS_EXPORTED_METRICS)
    assert all(has_all_metrics(el) for el in metrics)

    metric_names = [m["name"] for m in metrics]
    some_expected_symbols = [
        "stocks.WORK-latestPrice",
        "stocks.NFLX-latestPrice",
        "stocks.AMZN-latestPrice",
    ]

    assert all(symbol in metric_names for symbol in some_expected_symbols)
    print(metrics)
