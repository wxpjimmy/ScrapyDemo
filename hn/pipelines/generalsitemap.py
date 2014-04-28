from scrapy import log
from hn.utils.es_api import *
import redis
from datetime import datetime, timedelta
import traceback


class GeneralSitemapPipeline(object):

    ES_SERVER = "localhost"
    ES_PORT = '9200'
    ES_INDEX = 'test'
    ES_DOC_TYPE = 'perf'

    Time_Format = '%Y-%m-%d %H:%M:%S'

    def __init__(self, server):
        self.es = ES({self.ES_SERVER: self.ES_PORT}, self.ES_INDEX, self.ES_DOC_TYPE)
        self.server = server
        self._name = 'GeneralSitemapPipeline'

    def open_spider(self, spider):
        settings = spider.settings.get('PIPELINE_SPIDERS')
        process = spider.name in settings[self._name]
        if process:
            key = str(spider)
            log.msg("Open Spider [%s] in GeneralSitemapPipeline." % key)
            cached = self.server.get(key)
            if cached is None:
                now = datetime.utcnow()
                start = now - timedelta(days=7)
                self.lastmodified = datetime(start.year, start.month, start.day)
            else:
                self.lastmodified = datetime.strptime(cached, self.Time_Format)

            self.cur_max = self.lastmodified

    @classmethod
    def from_settings(cls, settings):
        cls.MONGODB_SERVER = settings.get('ES_SERVER', 'localhost')
        cls.MONGODB_PORT = settings.getint('ES_PORT', 9200)
        cls.ES_INDEX = settings.get('ES_INDEX', 'test')
        cls.ES_DOC_TYPE = settings.get('ES_DOC_TYPE', 'perf')
        host = settings.get('REDIS_HOST', 'localhost')
        port = settings.get('REDIS_PORT', 6379)
        server = redis.Redis(host, port)
        return cls(server)

    @classmethod
    def from_crawler(cls, crawler):
        cls.stats = crawler.stats
        return cls.from_settings(crawler.settings)
    
    def process_item(self, item, spider):
        settings = spider.settings.get('PIPELINE_SPIDERS')
        process = spider.name in settings[self._name]
        if process:
            update = item.get('update')
            if update:
                if self.lastmodified < update:
                    self._index_page(item, update, spider._type)
                    if self.cur_max < update:
                        self.cur_max = update

            else:
                # not time stamp found
                self._index_page(item, update, spider._type)
        return item

    def _index_page(self, item, update, type, bulk = True):
        try:
            if bulk:
                resp = self.es.index(item['link'], item['content'], item.get('title'), update, type, bulk)
                self.bulk_opt(resp)
            else:
                data = self.es.index(item['link'], item['content'], item.get('title'), update, type, bulk)
                created = data["created"]
                version = data["_version"]
                if created & version==1:
                    log.msg("[%s] [no_time] create Index for url: %s" % (spider, item['link']), log.DEBUG)
                elif version > 1:
                    log.msg("[%s] [no_time] update Index for url: %s" % (spider, item['link']), log.DEBUG) 
        except Exception, e:
            log.msg("Index Error: %s" % e, log.ERROR)
            traceback.print_exc()
        else:
            pass
        finally:
            pass
     

    def bulk_opt(self,resp):
        if resp:
            log.msg("Bulk index happened!", log.WARNING)
            succeed, errors = resp
            if isinstance(errors, int):
                err_count = errors
            else:
                err_count = len(errors)
            log.msg("Bulk index succeed: %d,  failed: %d" % (succeed, err_count), log.WARNING)        


    def close_spider(self, spider):
        settings = spider.settings.get('PIPELINE_SPIDERS')
        process = spider.name in settings[self._name]
        if process:
            key = str(spider)
            if len(self.es.actions) > 0:
                resp = self.es.bulk_index(spider._type)
                self.bulk_opt(resp)
            #no update found, use current utc time as the update time
            if self.cur_max == self.lastmodified:
                self.cur_max = datetime.utcnow()
            log.msg("Saving lastupdate[%s] to redis." % self.cur_max)
            self.server.set(key, self.cur_max.strftime(self.Time_Format))
            log.msg("Close Spider [%s] in GeneralSitemapPipeline." % key)

