from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch('http://localhost:9200')

def search_index(index_name, match_name):
    terms = " OR ".join(match_name.split())
    s = Search(index=index_name).using(client).query("query_string", query=terms).extra(size=10000)
    response = s.execute()
    return response

