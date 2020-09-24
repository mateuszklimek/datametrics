import pdb
import transform
from settings import CRYPTO_TO_TRACK, CRYPTO_EXPORTED_METRICS, STOCKS_TO_TRACK, STOCKS_EXPORTED_METRICS
import json


def has_all_metrics(el):
    return all(metric in el for metric in ['name', 'value', 'interval', 'time'])


def test_parsing_livecoin():

    with open('tests_data/sample_livecoin.json') as f:
        data = json.load(f)
    
    metrics = transform.livecoin_to_metrics(data)

    assert len(metrics) == len(CRYPTO_TO_TRACK) * len(CRYPTO_EXPORTED_METRICS)
    assert all(has_all_metrics(el) for el in metrics)
    print (metrics)
        

def test_parsing_iex():

    with open('tests_data/sample_iex.json') as f:
        data = json.load(f)

    metrics = transform.iex_to_metrics(data)

    assert len(metrics) == len(STOCKS_TO_TRACK) * len(STOCKS_EXPORTED_METRICS)
    assert all(has_all_metrics(el) for el in metrics)
    print (metrics)


if __name__ == "__main__":
    test_parsing_livecoin()
    test_parsing_iex()

    print ("Tests successfully passed!")