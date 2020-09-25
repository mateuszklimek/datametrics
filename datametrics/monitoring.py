from typing import Dict, List
from requests.models import Response

from datametrics import graphite


def health_check_response(service: str, response: Response) -> List[Dict]:
    health_metrics = graphite.get_health_metrics_from_response(service, response)

    if response.status_code != 200:
        print("Exception:", response.status_code, response.text)

        graphite.send_data([], health_metrics=health_metrics)
        raise Exception(response.text)

    return health_metrics
