from bs4 import BeautifulSoup as bs
from scrapy.spider import Spider
from scrapy.http import Request, XmlResponse
from hn.items import TcNewItem
from ElasticsearchClient import ES
import re
import os
import datetime
from scrapy import log
from scrapy.utils.sitemap import Sitemap, sitemap_urls_from_robots
from scrapy.utils.gz import gunzip, is_gzipped
from sitemap_util import *
import logging
from scrapy.log import ScrapyFileLogObserver


class GeneralSitemapSpider(Spider):
    name = 'sitemap'

    start_urls = []

    def __init__(self, s_type=None, **kwargs):
        if s_type is None:
            raise Exception("Must specify a spider type!")
        else:
            self._type = s_type
            print s_type
            time =  datetime.datetime.now()
            logfile = "scrapy_%s_%s_%s.log" % (self.name, self._type,time)
            print logfile
            handle = open(logfile, 'w')
            log_observer = ScrapyFileLogObserver(handle, level=logging.DEBUG)
            log_observer.start()
            
            error_file = "scrapy_%s_%s_%s_Error.log" % (self.name, self._type, time)
            error_handle = open(error_file, 'w')
            error_observer = ScrapyFileLogObserver(error_handle, level=logging.WARNING)
            error_observer.start()

            # load urls, load last crawled time
        super(GeneralSitemapSpider, self).__init__(self.name, **kwargs)

    def start_requests(self):
        urls = SM_URL.get(self._type)
        #log.msg(urls, level=log.INFO)
        #log.msg(urls, level=log.DEBUG)
        #log.msg(urls, level=log.WARNING)
        print urls
        #log.msg("Test warning/error log", logging.WARNING)
        for url in urls:
            yield Request(url, callback=self._parse_sitemap)


    def _parse_sitemap(self, response):
        print response.url
        if response.url.endswith('/robots.txt'):
            for url in sitemap_urls_from_robots(response.body):
                yield Request(url, callback=self._parse_sitemap)
        else:
            body = self._get_sitemap_body(response)
            if body is None:
                log.msg(format="Ignoring invalid sitemap: %(response)s",
                        level=log.WARNING, spider=self, response=response)
                return

            s = Sitemap(body)
            print s.type
            if s.type == 'sitemapindex':
                data = bs(body)
                locs = data.find_all('loc')
                print len(locs)
                for link in self._filter_loc(locs):
                    print link
                    if link is None:
                        print "find empty link: ", link
                    else:
                        yield Request(link, callback=self._parse_sitemap)
            elif s.type == 'urlset':
                func = SM_FUNC.get(self._type)
                print func.__name__
                for req in func(self, body):
                    yield req
    
    def process_page(self, response):
        func = PAGE_FUNC.get(self._type)
        print func.__name__
        for item in func(response):
            yield item

    def _filter_loc(self, locs):
        log.msg("filter starts")
        rules = SM_FILTER.get(self._type)
        if rules is None:
            log.msg("no rule found")
            for item in locs:
                print item
                yield item.string
        else:
            print rules
            for item in locs:
                should_filter = False
                for rule in rules:
                    ptn = re.compile(rule, re.IGNORECASE)
                    match = ptn.match(item.string)
                    if match is not None:
                        should_filter = True
                        break
                if should_filter:
                    continue
                else:
                    yield item.string



    def _get_sitemap_body(self, response):
        """Return the sitemap body contained in the given response, or None if the
        response is not a sitemap.
        """
        print "entering get sitemap body"
        if isinstance(response, XmlResponse):
            return response.body
        elif is_gzipped(response):
            return gunzip(response.body)
        elif response.url.endswith('.xml'):
            return response.body
        elif response.url.endswith('.xml.gz'):
            return gunzip(response.body)
        elif response.url.endswith('.xmlo'):
            return response.body

    def __str__(self):
        return "%s_%s" % (self.name, self._type)
