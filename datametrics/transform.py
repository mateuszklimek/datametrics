from datametrics.graphite import get_metric_values
from datametrics import settings
from typing import List, Dict


def iex_to_metrics(json_response: Dict) -> List[Dict]:
    data_to_export = []

    for symbol in json_response.keys():
        data_to_export.extend(
            get_metric_values(
                "stocks",
                symbol,
                json_response[symbol]["quote"],
                settings.STOCKS_EXPORTED_METRICS,
            )
        )

    return data_to_export


def livecoin_to_metrics(json_response: Dict) -> List[Dict]:
    symbols_exported = [
        f"{el}/{settings.CRYPTO_COMPARE_CURRENCY}" for el in settings.CRYPTO_TO_TRACK
    ]
    data_to_export = []

    for crypto_el in json_response:
        if crypto_el["symbol"] in symbols_exported:

            data_to_export.extend(
                get_metric_values(
                    "crypto",
                    crypto_el["symbol"],
                    crypto_el,
                    settings.CRYPTO_EXPORTED_METRICS,
                )
            )

    return data_to_export
