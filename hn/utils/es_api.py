from elasticsearch import Elasticsearch
import json
from datetime import datetime
import time
from scrapy import log

def timeit(func):
    def wrap(*args):
        time1 = time.time()
        ret = func(*args)
        time2 = time.time()
        log.msg('%s function took %0.3f ms' % (func.func_name, (time2-time1)*1000.0), log.DEBUG)
        # should replace the printing with record to StatsD(categorized by func_name)
        return ret
    return wrap


class ES(object):
    """
    Elasticsearch API wrapper
    """
    def __init__(self, nodes, index=None, doc_type=None):
        self.instance = Elasticsearch(hosts=nodes)
        self._index = index or 'ivy'
        self._doc_type = doc_type or 'webpage'

    def __build_index_content(self, url, content, title, update):
        req = {"url":url, "data":content}
        if title:
            req["title"] = title

        if update:
            req["update"] = update.strftime('%Y-%m-%d %H:%M:%S')
        else:
            req["update"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        return req

    def __build_search_content(self, text):
        return {"query":
                    {"match":
                        {"data":
                            {"query": text, "minimum_should_match": "80%"}
                        }
                    }
                }

    def __parse_index_response(self, data, s_type):
        """
        pase the index response
        if first time insert, created should be true and version should be 1
        if not first time insert(index update), created is false and version should be larger than 1
        """
        created = data["created"]
        version = data["_version"]
        # metrics here to calculate unique page by s_type
        if version > 1:
            return True
        return created & (version==1)

    def __parse_search_response(self, data):
        """
        parse the search response
        return format {"cost": xxx, "result": [{"url": "http://...", "score": 0.45}, {...}, ]}
        """
        result = []
        hits = data["hits"]["hits"]
        cost = data["took"]
        for record in hits:
            res = {}
            score = record["_score"]
            url = record["_source"]["url"]
            res["url"] = url
            res["score"] = score
            result.append(res)
        return {"cost": cost, "result":result}

    @timeit
    def index(self, url, content, title, update, s_type):
        """
        index url and content with default index and doc_type
        """
        return self.index_customize(self._index, self._doc_type, url, content,title, update, s_type)

    def index_customize(self, index, doc_type, url, content, title, update, s_type):
        """
        index url and content with specified index and doc_type
        """
        data = self.__build_index_content(url, content, title, update)
        h_id = hex(hash(url))
        #exist = self.instance.exists(index = self._index, doc_type = self._doc_type, id = h_id)
        p = self.instance.index(index=index, doc_type=doc_type, id=h_id, body=data)
        if not self.__parse_index_response(p, s_type):
            log.msg("Error occurred when indexing: %s; Results: %s" % (url, p), log.ERROR)
        return p

    @timeit
    def search(self, text, needwrap):
        """
        search the default index and doc_type
        text is the query content
        if needwrap is true, text should be just the keyword(s) you want to query
        if needwrap is false, text should be a formatted elasticsearch query
        """
        return self.search_index_type(self._index, self._doc_type, text, needwrap)

    @timeit
    def search_all(self, text, needwrap):
        """
        search in all es index and doc_type
        """
        data = text
        if needwrap:
            data = self.__build_search_content(text)
        raw = self.instance.search(body=data, _source_include=['url'], size=5)
        return self.__parse_search_response(raw)

    @timeit
    def search_customize(self, index, doc_type, data, analyzer, _source_include, _source_exclude, size):
        """
        search with specified index, doc_type, analyzer, _source_include, _source_exclude and result max size
        """
        raw = self.instance.search(index=index, doc_type=doc_type, body=data, analyzer=analyzer, _source_include=_source_include
            , _source_exclude=_source_exclude, size=size)
        return self.__parse_search_response(raw)

    
    def search_index_type(self, index, doc_type, text, needwrap):
        """
        search with specified index and doc_type
        """
        data = text
        if needwrap:
            data = self.__build_search_content(text)
        raw = self.instance.search(index=index, doc_type=doc_type, body=data, _source_include=['url'], size=5)
        return self.__parse_search_response(raw)