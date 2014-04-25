from scrapy import log
from hn.utils.es_api import *
import redis
from datetime import datetime, timedelta


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
    def from_crawler(cls, crawler):
        cls.MONGODB_SERVER = crawler.settings.get('ES_SERVER', 'localhost')
        cls.MONGODB_PORT = crawler.settings.getint('ES_PORT', 9200)
        cls.ES_INDEX = crawler.settings.get('ES_INDEX', 'test')
        cls.ES_DOC_TYPE = crawler.settings.get('ES_DOC_TYPE', 'perf')
        host = crawler.settings.get('REDIS_HOST', 'localhost')
        port = crawler.settings.get('REDIS_PORT', 6379)
        server = redis.Redis(host, port)
        pipe = cls(server)
        pipe.crawler = crawler
        return pipe
    
    def process_item(self, item, spider):
        settings = spider.settings.get('PIPELINE_SPIDERS')
        process = spider.name in settings[self._name]
        if process:
            update = item.get('update')
            if update:
                if self.lastmodified < update:
                    self.es.index(item['link'], item['content'], item.get('title'), update, spider._type);
                    log.msg("[%s] create Index for url: %s" % (spider, item['link']), log.DEBUG)
                    if self.cur_max < update:
                        self.cur_max = update

            else:
                # not time stamp found
                data = self.es.index(item['link'], item['content'], item.get('title'), update, spider._type);
                created = data["created"]
                version = data["_version"]
                if created & version==1:
                    log.msg("[%s] [no_time] create Index for url: %s" % (spider, item['link']), log.DEBUG)
                elif version > 1:
                    log.msg("[%s] [no_time] update Index for url: %s" % (spider, item['link']), log.DEBUG)

        return item

    def close_spider(self, spider):
        settings = spider.settings.get('PIPELINE_SPIDERS')
        process = spider.name in settings[self._name]
        if process:
            key = str(spider)
            log.msg("Saving lastupdate[%s] to redis." % self.cur_max)
            self.server.set(key, self.cur_max.strftime(self.Time_Format))
            log.msg("Close Spider [%s] in GeneralSitemapPipeline." % key)

