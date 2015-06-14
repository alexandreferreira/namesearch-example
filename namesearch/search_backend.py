__author__ = 'alexandreferreira'
from haystack.backends.elasticsearch_backend import ElasticsearchSearchBackend, ElasticsearchSearchEngine

class CustomElasticsearchSearchBackend(ElasticsearchSearchBackend):
    DEFAULT_SETTINGS = {
        'settings': {
            "analysis": {
                "analyzer": {
                    "ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "lowercase",
                        "filter": ["haystack_ngram"]
                    },
                    "edgengram_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["standard", "lowercase", "haystack_edgengram"]
                    }
                },
                "tokenizer": {
                    "haystack_ngram_tokenizer": {
                        "type": "nGram",
                        "min_gram": 3,
                        "max_gram": 15,
                    },
                    "haystack_edgengram_tokenizer": {
                        "type": "edgeNGram",
                        "min_gram": 2,
                        "max_gram": 15,
                    }
                },
                "filter": {
                    "haystack_ngram": {
                        "type": "nGram",
                        "min_gram": 3,
                        "max_gram": 15
                    },
                    "haystack_edgengram": {
                        "type": "edgeNGram",
                        "min_gram": 2,
                        "max_gram": 15
                    }
                }
            }
        }
    }

class CustomElasticsearchSearchEngine(ElasticsearchSearchEngine):
    backend = CustomElasticsearchSearchBackend