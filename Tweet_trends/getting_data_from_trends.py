from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import pandas as pd
es = Elasticsearch(host='localhost', port=9200)
def get_data_from_elastic(search_trending_hashtag):
    # query: The elasticsearch query.
    response = []
    query = {
            "query": {
            "bool": {
            "must": {
                "bool" : { 
                "must": [
                    {
                    "query_string": {
                        "fields": ["text","description","hashtags.text"],
                        "query": search_trending_hashtag
                    }
                    },
                ]
                }
            }
            }
        },
        "sort": [
            { "created_at": "asc" }
            ]
        }
    basic_data = es.search(index="trending_hashtags_tweets", scroll = "2m",body=query,size=10000)
    if basic_data and basic_data['hits']['hits']:
        if len(basic_data['hits']['hits'])>=1:
            response.extend(basic_data['hits']['hits'])
        else:
            response.extend(basic_data['hits']['hits'])
        return response
df = get_data_from_elastic("Newsom")
print(df)