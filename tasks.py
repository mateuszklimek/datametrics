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
    "run-me-every-ten-seconds": {
    "task": "tasks.submit_metrics",
    "schedule": 60.0
    }
}

@app.task
def submit_metrics():
    response = requests.get(settings.LIVE_COIN_API_URL)
    json_response = response.json()
    for el in json_response:
        if el['symbol'] == 'BTC/USD':
            
            data = [{
                "name": "crypto.btc_usd",
                "value": el['last'],
                "interval": 1,
                "time": int(datetime.datetime.now().timestamp())
            }]

            response = requests.post(
                settings.GRAPHITE_URL,
                json=data,
                auth=HTTPBasicAuth(settings.GRAPHITE_USER, settings.GRAPHITE_PASSWORD)
            )
            print (response.text)
