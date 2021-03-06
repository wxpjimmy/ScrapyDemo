from bs4 import BeautifulSoup as bs
from scrapy.spider import Spider
from scrapy.http import Request
from hn.items import TcNewItem
import re
import os
import datetime

class TcNewSpider(Spider):
    name = 'tcnew'

    start_urls = ['http://techcrunch.com/sitemap.xml' ]

#    sitemap_rules = [('.*yyyy=\d{4}&mm=\d{2}&dd=\d{2}', 'parse_eachday'),
#            ('.*/\d{4}/\d{2}/\d{2}/.*', 'parse_content'),
#            ('.*/tag/.*', 'parse_content')]
#            ('.*', 'parse_page')]

    def __init__(self, **kwargs):
        super(TcNewSpider, self).__init__(self.name, **kwargs)
        self._last = datetime.datetime(1970,1,1)
        self._origin = datetime.datetime(1970, 1, 1)
        exist = os.path.isfile('/Users/jimmy/lastcrawled.txt')
        print exist
        if exist:
            handler = open('/Users/jimmy/lastcrawled.txt', 'r+')
            txt = handler.readline()
            print txt
            handler.close()
            self._last = datetime.datetime.strptime(txt.strip(), '%Y-%m-%d %H:%M:%S')

    def parse(self, response):
        print "parse: ", response.url
        data = bs(response.body)

        if self._last > self._origin:
            pt = '.*yyyy=(\d{4})&mm=(\d{2})&dd=(\d{2})'
            pattern = re.compile(pt)
            for url in data.find_all('loc'):
                match = pattern.match(url.string)
                dt = datetime.datetime(int(match.group(1)), 
                        int(match.group(2)), int(match.group(3)))
                if dt < self._last:
                    pass
                else:
                    yield Request(url.string, callback=self.parse_eachday)

        else:
            for url in data.find_all('loc'):
                yield Request(url.string, callback=self.parse_eachday)

    def parse_eachday(self, response):
        url = response.url
        data = bs(response.body)
        print "Parse root level page: ", url

        for sec in data.find_all('url'):
            link = sec.loc.string
            lastmod = sec.lastmod.string
            item = TcNewItem()
            item['update'] = lastmod
            request = Request(link, callback=self.parse_content)
            request.meta['item'] = item
            yield request

    def parse_content(self, response):
        url = response.url
        data = response.body
        tc_item = response.meta['item']
        tc_item['link'] = url
        tc_item['content'] = data
        print("Finished download url: %s, len: %d" % (url, len(data)))
        return tc_item
        print 'pipeline init'

    def __str__(self):
        return self.name
