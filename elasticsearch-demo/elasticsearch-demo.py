from elasticsearch import Elasticsearch
import requests
es = Elasticsearch("https://elastic:kpJCLVvYi1aOwtBliI+x@localhost:9200")


# here we fetch an example dataset from discogs.com to our elasticsearch
def discogs_requester(item_number):
    api_url = 'https://api.discogs.com'
    what_we_dig = 'masters'
    request_url = f'{api_url}/{what_we_dig}/{item_number}'
    user_token = 'dYIKKqaiuAioKjgITGwSTbOVYLGfOrTxwNWugZCR'

    # discogs API limits the frequency of requests to 60 per minute, so I set the timeout here
    response = requests.get(request_url, params={'token':user_token}, timeout=2)

    return response.json()


def elastic_putter(item_number, discogs_item):
    es.index(index='discogs_master_releases', id=item_number, document=discogs_item)


def copypaster():
    for item_number in range(19016,22600):
        current_item = discogs_requester(item_number=item_number)
        elastic_putter(item_number=item_number, discogs_item=current_item)


# to play with this data we're better off with Jupyter Notebook

if __name__ == "__main__":
    copypaster()
