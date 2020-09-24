import os

REDIS_URL = os.environ["REDIS_URL"]

GRAPHITE_USER = os.environ["GRAPHITE_USER"]
GRAPHITE_PASSWORD = os.environ["GRAPHITE_PASSWORD"]

GRAPHITE_URL = "https://graphite-us-central1.grafana.net/metrics"
LIVE_COIN_API_URL = "https://api.livecoin.net/exchange/ticker"

IEX_CLOUD_API_TOKEN = os.environ["IEX_CLOUD_API_TOKEN"]
IEX_CLOUD_API_URL = "https://cloud.iexapis.com/v1/stock/market/batch"

CRYPTO_COMPARE_CURRENCY = "USD"
CRYPTO_TO_TRACK = ["BTC", "ETH", "BAT"]
CRYPTO_EXPORTED_METRICS = ["last", "high", "low", "vwap", "volume"]

STOCKS_TO_TRACK = ["AMZN", "WORK", "NFLX"]
STOCKS_EXPORTED_METRICS = ["latestPrice", "iexAskPrice", "iexBidPrice"]

CELERY_TASKS_TO_RUN = {
    "send_crypto_metrics": {
        "task": "datametrics.tasks.send_livecoin_to_graphite",
        "schedule": 60.0,
    },
    "send_stocks_metrics": {"task": "datametrics.tasks.send_stocks_to_graphite", "schedule": 60.0},
}
CELERY_APP_NAME = "celery_metrics_sender"
