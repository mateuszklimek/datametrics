import celery
import requests
import graphite
import transform
import settings

app = celery.Celery('celery_metrics_sender')

app.conf.update(BROKER_URL=settings.REDIS_URL,
                CELERY_RESULT_BACKEND=settings.REDIS_URL)

app.conf.CELERYBEAT_SCHEDULE = {
    "send_crypto_metrics": {
        "task": "tasks.send_livecoin_to_graphite",
        "schedule": 60.0
    },
    "send_stocks_metrics": {
        "task": "task.send_stocks_to_graphite",
        "schedule": 60.0
    }
}

@app.task
def send_stocks_to_graphite():
    stocks_str = ','.join(settings.STOCKS_TO_TRACK)
    response = requests.get(
        f'{settings.IEX_CLOUD_API_URL}?types=quote&symbols={stocks_str}&token={settings.IEX_CLOUD_API_TOKEN}'
    )

    data_to_export = transform.iex_to_metrics(response.json())
    graphite.send_data(data_to_export)


@app.task
def send_livecoin_to_graphite():
    response = requests.get(settings.LIVE_COIN_API_URL)

    data_to_export = transform.livecoin_to_metrics(response.json())
    graphite.send_data(data_to_export)

