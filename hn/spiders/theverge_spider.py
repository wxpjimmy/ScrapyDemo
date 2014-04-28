from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
import re
from bs4 import BeautifulSoup as bs
from hn.items import SitemapItem
import datetime

class TheVergeSpider(CrawlSpider):
    name='theverge'
    start_urls = ['http://www.theverge.com']

    rules = (
            Rule(SgmlLinkExtractor(allow=(r'http://www.theverge.com/\d{4}/\d{1,2}/\d{1,2}/.*')), callback='process_article'),
            Rule(SgmlLinkExtractor(allow=(r'http://www.theverge.com/\w+$', r'http://www.theverge.com/us-world$'), 
                deny=(r'http://www.theverge.com/.*/.*', r'/search', r'/forums', r'/longform', r'video', r'/jobs', r'/archives'))),
#            Rule(SgmlLinkExtractor(allow=(r'/.*/archives$', r'/.*/archives/\d+$'))),
            )


    def _init__(self, **kwargs):
        super(TheVergeSpider, self).__init__(self.name, **kwargs)
        pass

    def process_article(self, response):
        item = SitemapItem()
        url = response.url
        pattern = re.compile(r'http://www.theverge.com/(\d{4})/(\d{1,2})/(\d{1,2})/.*')
        match = pattern.match(url)
        dt = datetime.datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        print dt
        #test if the item should be processed
        item['link'] = url
#        item['content'] = response.body
        return item

    def __str__(self):
        return self.name
