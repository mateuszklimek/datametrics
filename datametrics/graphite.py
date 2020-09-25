import requests
import datetime
from requests.auth import HTTPBasicAuth
from requests.models import Response
from typing import Dict, List

from datametrics import settings


def get_epoch_in_seconds() -> int:
    return int(datetime.datetime.now().timestamp())


def send_data(data: List[Dict], health_metrics: List[Dict] = None):

    to_send = (data or []) + (health_metrics or [])

    print("sending data:", to_send)

    response = requests.post(
        settings.GRAPHITE_URL,
        json=to_send,
        auth=HTTPBasicAuth(settings.GRAPHITE_USER, settings.GRAPHITE_PASSWORD),
    )

    if response.status_code != 200:
        # TODO Proper handling of http exceptions logging and alerting on them
        print("Exception:", response.status_code, response.text)

    print(response.text)


def get_metric_values(
    metric_type: str, metric_symbol: str, dict_el: Dict, metrics_values: List
) -> List[Dict]:
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


def get_health_metrics_from_response(name: str, response: Response) -> List[Dict]:
    time_metric = {
        "name": f"metrics.{name}.response.time",
        "value": response.elapsed.total_seconds(),
        "interval": 1,
        "time": get_epoch_in_seconds(),
    }

    response_time_metric = {
        "name": f"metrics.{name}.response.status_code",
        "value": response.status_code,
        "interval": 1,
        "time": get_epoch_in_seconds(),
    }

    return [time_metric, response_time_metric]
