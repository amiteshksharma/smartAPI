import json
import os

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index
from model import APIDoc, APIMeta

_dirname = os.path.dirname(__file__)
with open(os.path.join(_dirname, 'mapping.json'), 'r') as file:
    SMARTAPI_MAPPING = json.load(file)


def setup():
    """
    Setup Elasticsearch Index.
    Primary index with dynamic template.
    Secondary index with static mappings.
    """

    if not Index(APIDoc.Index.name).exists():
        elastic = Elasticsearch()
        elastic.indices.create(
            index=APIDoc.Index.name,
            body=SMARTAPI_MAPPING
        )
        APIDoc.init()

    if not Index(APIMeta.Index.name).exists():
        APIMeta.init()


def reset():

    index = Index(APIDoc.Index.name)

    if index.exists():
        index.delete()

    index = Index(APIMeta.Index.name)

    if index.exists():
        index.delete()

    setup()


def refresh():

    index = Index(APIDoc.Index.name)
    index.refresh()
    index = Index(APIMeta.Index.name)
    index.refresh()
