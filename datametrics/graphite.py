import requests
import datetime
from requests.auth import HTTPBasicAuth
from typing import Dict, Sequence

from datametrics import settings


def get_epoch_in_seconds() -> int:
    return int(datetime.datetime.now().timestamp())


def send_data(data: Sequence[Dict]):
    print("sending data:", data)

    # TODO: There are more efficient formats than json (to send data) available.
    # It's possible it's worth changing to them in case more efficient transfer
    # is needed (etc. much bigger amounts of data are sent)
    response = requests.post(
        settings.GRAPHITE_URL,
        json=data,
        # TODO: Consider other auth methods
        auth=HTTPBasicAuth(settings.GRAPHITE_USER, settings.GRAPHITE_PASSWORD),
    )

    if response.status_code != 200:
        # TODO Proper handling of http exceptions logging and alerting on them
        print("Exception:", response.status_code, response.text)

    print(response.text)


def get_metric_values(
    metric_type: str, metric_symbol: str, dict_el: Dict, metrics_values: Sequence
) -> Sequence[Dict]:
    data = [
        {
            "name": "{}.{}-{}".format(metric_type, metric_symbol, key),
            "value": dict_el[key],
            "interval": 1,
            "time": get_epoch_in_seconds(),
        }
        for key in metrics_values
    ]

    return data
