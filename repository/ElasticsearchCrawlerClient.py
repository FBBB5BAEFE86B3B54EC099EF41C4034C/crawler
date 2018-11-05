from elasticsearch import Elasticsearch
from elasticsearch import exceptions
import time
import datetime
import json

class ElasticsearchCrawlerClient(object):
    """ElasticsearchCrawlerClient is a CrawlerClient for Elasticsearch."""

    def __init__(self, url):
        """ElasticsearchCrawlerClient Constructor"""
        print(url)
        self.es = Elasticsearch(url)
        self.bufferindex = "bufferindex"
        self.fulltextindex = "fulltext"

    def contains(self, key):
        """External method 'contains' - checks, if this key already exists in Elasticsearch. Uses '__contains'."""
        self.__contains(self.fulltextindex, "all", key)

    def __contains(self, index, doc_type, key):
        """Internal method '__contains' - checks, if this key already exists in Elasticsearch."""
        try:
            res = self.es.get(index=index, doc_type=doc_type, id=key)
            print(res)
            print(res['_source'])
            return True
        except exceptions.NotFoundError as error:
            print(error)
            if error.status_code == 404:
                return False
            else:
                raise error

    def put(self, key, data, date, tags, head, index="fulltext"):
        """External method 'put' - puts data to Elasticsearch. Uses '__put'."""
        doc = {
            'key': key,
            'data': data,
            'date': date,
            'tags': tags,
            'head': head,
            'timestamp': datetime.datetime.now()
        }
        print(doc)
        self.__put(index, "all", key, doc)

    def __put(self, index, doc_type, key, body):
        """Internal method '__put' - puts data to Elasticsearch."""
        try:
            res = self.es.index(index=index, doc_type=doc_type, id=key, body=body, refresh=True)
            self.buffer_put(index=self.bufferindex, doc_type=doc_type, key=key, body=body)
            print(res)
            return res
        except exceptions as error:
            print("ERROR:"+error)
            raise error

    def buffer_put(self, index, doc_type, key, body):
        """Internal method '__put' - puts data to Elasticsearch."""
        try:
            res = self.es.index(index=index, doc_type=doc_type, id=key, body=body, refresh=True)
            print(res)
            return res
        except exceptions as error:
            print("ERROR:" + error)
            raise error

    def search(self, index, doc_type="all", size=10):
        """External method 'search' - searches data in Elasticsearch."""
        res = self.es.search(index=index, doc_type=doc_type, size=size)
        # print(res['hits']['hits'])
        parsed = json.loads(json.dumps(res))
        print(json.dumps(parsed, indent=4, sort_keys=True))
        return res

    def index(self, index):
        """External method 'index' - creates index in Elasticsearch."""
        try:
            res = self.es.indices.create(index=index)
            return res
        except exceptions.RequestError as error:
            if str(error).find("resource_already_exists_exception"):
                print("resource_already_exists_exception")
            else:
                raise error

    def delete_index(self, index):
        """External method 'delete' - deletes index in Elasticsearch."""
        self.es.indices.delete(index=index)

    def delete_document(self, index, doc_type, id):
        """External method 'delete' - deletes index in Elasticsearch."""
        try:
            self.es.delete(index=index, doc_type=doc_type, id=id, refresh=True)
            print("Document is successfully deleted!")
        except exceptions.RequestError as error:
            raise error

    def exists(self, index):
        """External method 'exists' - exists index in Elasticsearch."""
        res = self.es.exists(index)
        print(res['_source'])

    def get(self, index):
        """External method 'get' - gets index in Elasticsearch."""
        res = self.es.get(index=index)
        print(res['_source'])
        return res

    def scroll_search(self, index="_all"):
        """External method 'search' - searches data in Elasticsearch.
        https: // stackoverflow.com / questions / 46604207 / elasticsearch - scroll
        """
        res = self.es.search(
            index=index,
            doc_type='all',
            scroll='10s',
            size=100,
            body={
                # Your query's body
            })
        parsed = json.loads(json.dumps(res))
        print(json.dumps(parsed, indent=4, sort_keys=True))
        sid = res['_scroll_id']
        print(sid)
        print(res['hits']['total'])
        return sid

    def scroll(self, scroll_id):
        while True:
            time.sleep(5)
            res = self.es.scroll(scroll_id=scroll_id)
            print(json.dumps(json.loads(json.dumps(res)), indent=4, sort_keys=True))
            self.put(key=datetime.datetime.now(), data="Some data here!", date="2018.11.02", tags=["tag0", "tag1", "tag2"], index="tag100500")

class ElasticsearchCrawlerClientFactory(object):

    def __init__(self, url = "http://127.0.0.1:9300/"):
        self.url = url
        self.clientSingleton = ElasticsearchCrawlerClient(self.url)

    def getSingleton(self):
        return self.clientSingleton


    def getPrototype(self):
        return ElasticsearchCrawlerClient(self.url)

