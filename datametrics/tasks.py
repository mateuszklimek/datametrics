import celery
import requests
from datametrics import graphite, transform, settings, monitoring

app = celery.Celery(settings.CELERY_APP_NAME)
app.conf.update(BROKER_URL=settings.REDIS_URL, CELERY_RESULT_BACKEND=settings.REDIS_URL)
app.conf.CELERYBEAT_SCHEDULE = settings.CELERY_TASKS_TO_RUN


@app.task
def send_stocks_to_graphite() -> None:
    stocks_str = ",".join(settings.STOCKS_TO_TRACK)

    response = requests.get(
        f"{settings.IEX_CLOUD_API_URL}?types=quote&symbols={stocks_str}&token={settings.IEX_CLOUD_API_TOKEN}"
    )

    health_metrics = monitoring.health_check_response("iex", response)

    data_to_export = transform.iex_to_metrics(response.json())
    graphite.send_data(data_to_export, health_metrics=health_metrics)


@app.task
def send_livecoin_to_graphite() -> None:
    response = requests.get(settings.LIVE_COIN_API_URL)

    health_metrics = monitoring.health_check_response("livecoin", response)

    data_to_export = transform.livecoin_to_metrics(response.json())
    graphite.send_data(data_to_export, health_metrics=health_metrics)
