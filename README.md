# namesearch-example

This a example of a Django App using ElasticSearch

## Project

This is just a sample project to search for names in database.


## Celery Beats

- Import 1000 names (2 min)

## The run this project you have to set some envirounments

```sh
export BROKER_URL="amqp://username:password@HOST:port/NAME"
export DATABASE_URL="postgres://username:password@host:port/name"
export HAYSTACK_INDEX="name_index"
```

## Libraries used in this project

- Django
- Celery + Django-Celery
- ElasticSearch + Django-Haystack
- Select2
- Django Rest Framework
- Requests
