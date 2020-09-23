import requests
import datetime
from requests.auth import HTTPBasicAuth

import settings


def get_epoch_in_seconds():
    return int(datetime.datetime.now().timestamp())


def send_data(data):
    print ("sending data:", data)

    #TODO: There are more efficient formats than json (to send data) available.
    # It's possible it's worth changing to them in case more efficient transfer
    # is needed (etc. much bigger amounts of data are sent)
    response = requests.post(
        settings.GRAPHITE_URL,
        json=data,
        auth=HTTPBasicAuth(settings.GRAPHITE_USER, settings.GRAPHITE_PASSWORD)
    )
    print (response.text)


def get_metric_values(metric_type, dict_el, metrics_values):
    data = [
        {
            'name': '{}.{}-{}'.format(metric_type, dict_el['symbol'], key),
            'value': dict_el[key],
            'interval': 1,
            'time': get_epoch_in_seconds()
        }
        for key in metrics_values
    ]
    
    return data