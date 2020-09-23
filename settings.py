import os

REDIS_URL=os.environ['REDIS_URL']

GRAPHITE_USER=os.environ['GRAPHITE_USER']
GRAPHITE_PASSWORD=os.environ['GRAPHITE_PASSWORD']

GRAPHITE_URL='https://graphite-us-central1.grafana.net/metrics'
LIVE_COIN_API_URL='https://api.livecoin.net/exchange/ticker'

CRYPTO_TO_TRACK = ['BTC', 'ETH', 'LINK', 'BAT']
CRYPTO_EXPORTED_METRICS = ['last', 'high', 'low', 'vwap', 'volume']
