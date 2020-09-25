# DataMetrics

Pushing metrics (gathered from API/Internet) to graphite, to make them visible in Grafana.

## Architecture

Current projects setup looks like that:
There are celery tasks running every minute (could be configured to something more/less often in `settings.py`)
Tasks are doing calls to APIs to gather info about crypto and stock prices, transform received data to `graphite` metrics format and do HTTP requests with metrics (in `json` format using BasictAuth) to graphite.

## Running manual ingestion locally

To run/test ingestion locally you need to install requires, make sure your environment has variables needed by this project and then run python run_once script. Run `python run_once -h` for help. Current project was tested with `python 3.8.5`

```bash
pip install -r requirements.txt
export REDIS_URL=<REDIS_URL>
export GRAPHITE_USER=<GRAPHANA_BASIC_AUTH_USER>
export GRAPHITE_PASSWORD=<GRAPHANA_BASIC_AUTH_PASSWORD>
export IEX_CLOUD_API_TOKEN=<IEX_CLOUD_API_TOKEN>

python run_once.py --crypto --stocks
```

## Running using heroku and celery

Setup for deploying to heroku was made using instructions from here: [here](https://devcenter.heroku.com/articles/celery-heroku)

`Procfile` contains information about processes which will be run on heroku. Currently it's Celery worker and Celery beat

Once setup is done (app with redis created and enviroment variables setup),
to deploy app you need to commit changes to local repo and run

```bash
git push heroku master
```
You can view logs by doing:
```bash
heroku logs -t -p worker
```
//TODO: Possibly make a script for some standard setup to be done, it still requires some manual steps like setting up configs

## Scalability:

### Questions

**How to support much larger of metrics?** From code perspective it should be easy to add new sources/metrics by either just updating `settings.py` or  adding new Celery tasks with different sources. If number of metrics we want to track is often changing, I think good idea would be to create relational database with those metrics and make it used by tasks so that deployment is not needed to add new metrics.

**What if you needed to sample them more frequently?** Celery can run more often than every minute and it's just part of settings to run more frequently. But of course there maybe some issues if we decide to run it every second etc, current limitation being using HTTP to get/send data. So here it's possible we would need to switch to different methods to make it work properly.
https://graphite.readthedocs.io/en/latest/feeding-carbon.html#using-amqp

**Had many users accessing your dashboard to view metrics>** This is on Grafana side. Current plan support just 10 users (and 5$ for every other).
If it's to be open to the world, it's possible Grafana wouldn't be good choice, and some other frontend service querying possibly still Graphite would be necessary.
In those cases, it would be probably good to add some cache on top of Graphite to support usecase for very many simlar queries.
Some ideas to still go with Grafana would be to either use Grafana snopshots (which are publicly avialble just not refreshing) and build a service based on that (seems I bit hacky and not sure if easly possible).
Also with self hosted Grafana it's probably possible to do it for larger number of users with caching and multiple grafana instances. [Some suggestions here](https://community.grafana.com/t/how-many-concurrent-users-sessions-can-grafana-handle/11769)

### Storage 
Storing metrics is done only on `graphite` side, so to support much bigger number of metrics/data you need to make sure your graphite have space to that. With my current setup using GrafanaLabs I can store up to 100GB of logs there before being charged more.., but it should automatically scale with more usage. From what is see retention policies also ones which store data with less granularity are also possible to setup if we want to save on space stored: [https://graphite.readthedocs.io/en/latest/config-carbon.html](https://graphite.readthedocs.io/en/latest/config-carbon.html)

### Compute
For celery side, it is deployed on heroku. So simplest way of scaling up and make sure we have more compute for reading/parsing metrics gathered is to add dynos to your celery workers: `heroku ps:scale worker=more`. Overall I believe many celery tasks gathering various metrics could be run with this setup.

For Graphite/Grafana similary if they are just hosted by GrafanaLabs they should scale (use more resources) with more traffic //TODO look for more details on that

### Network
Celery can run multiple tasks at once gathering and publishing various metrics. Sending data to Grafite could be definitely make much more efficient with using some libraries specific for that (not HTTP requests) more details here: [here](https://graphite.readthedocs.io/en/latest/feeding-carbon.html). But one important thing to remember is Celery will be doing HTTP requests for external API, so it will probably not shorter that much live of Celery tasks. 

## Monitoring:

As Grafana is hosted in the cloud I think it can be mostly be assumed frontend side is working (Or doesn't but cannot be fixed by me)

So I think most important is making sure Celery processes are working properly and not receiving any errors when making requests to APIs and sending
proper data to Grafana.

**How would you track the health and uptime of your application?**
 
 - Grafana makes it possible to add alerts on dashboads (for example alerting if we didn't received any data on stock in last minute/5 minutes etc)
   To not create those manually for all things exported, it would be nice to create it automatically when adding new sources/stocks etc.
   I believe it requires creating dashbaord just for alerts and updating json of that dashbaord (to contain allerts required) when they are changes in metrics we export.

**What would you be measuring and alerting on*?

On Celery tasks side
- requests HTTP errors and response time (both from external API's and Graphite)
I would start with sending those to grafana and making dashboard for those logs there.

On Grafana side 
 - would be checking if data is coming, so alerting on situation when we didn't received new data for specific dashboards.
Those allerts are is something actually already added.
 - also could alert on some not expected data, for example for all crypto/stocks we can assume it will be larger than 0.
 - costs of running it :) and for that they actually have dashboard already prepared..

On Heroku side
 - some general Celery/redis performance metrics. Some of them are already available on Heroku.
 - Number of time tasks spend waiting on responses
 - Similarly to graphana potential costs, how close to limits in current plan we are, etc. 


## Running tests.

For running tests use py.test example:

```bash
py.test tests/*
```

## Code formatting

Project is using Black as code formatter, so before commiting make sure you run

```bash
black .
```

//TODO Add running black to precommit hooks


## Enviroment/Dev setup

Currently project does not have any setup to create/activate virtualenvs.
I'm using pyenv for this, but feel free to use whateher sounds best.

There is one setup script setup_dev.sh, which install requirements and package in dev mode.
So you can do install (when already on proper virtualenv)

```bash
./setup_dev.sh
```

// TODO setup.py is bare minimum doesn't have requirements specified for example

## Potential improvements
