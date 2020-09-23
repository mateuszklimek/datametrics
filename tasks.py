import celery
import os
import requests
import datetime
from requests.auth import HTTPBasicAuth
import settings

app = celery.Celery('celery_submit_app')
app.conf.update(BROKER_URL=settings.REDIS_URL,
                CELERY_RESULT_BACKEND=settings.REDIS_URL)
app.conf.CELERYBEAT_SCHEDULE = {
    "send_crypto_metrics": {
        "task": "tasks.send_livecoin_to_graphite",
        "schedule": 6.0
    }
}

def get_epoch_in_seconds():
    return int(datetime.datetime.now().timestamp())


def get_crypto_metrics(crypto_el):
    epoch_time = get_epoch_in_seconds()

    data = [
        {
            'name': 'crypto.{}-{}'.format(crypto_el['symbol'], key),
            'value': crypto_el[key],
            'interval': 1,
            'time': epoch_time
        }
        for key in settings.CRYPTO_EXPORTED_METRICS
    ]
    
    return data

def get_stock_metrics():
    pass


def send_data_to_graphite(data):
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


@app.task
def send_livecoin_to_graphite():
    response = requests.get(settings.LIVE_COIN_API_URL)
    json_response = response.json()

    symbols_exported = [
        '{}/USD'.format(el) for el in settings.CRYPTO_TO_TRACK
    ]
    data_to_export = []
    
    for crypto_el in json_response:
        if crypto_el['symbol'] in symbols_exported:
            
           data_to_export.extend(
               get_crypto_metrics(crypto_el)
           )

    send_data_to_graphite(data_to_export)

