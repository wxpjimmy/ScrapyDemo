from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from hn.items import CommonItem
from scrapy.http import Request
from general_util import *




class GeneralSpider(CrawlSpider):
    name = 'general'
    start_urls = []
    rules = ()
#    rules = (
#            Rule(SgmlLinkExtractor(deny=('\.js', '\.php', 'search.yahoo.com','yahoo.uservoice.com', '\?q=')), callback='parse_content', follow=True),
#            )


    def __init__(self, key=None, **kwargs):
        #fetch general to crawl list here from file or DB
        if key is None:
            raise Exception("No start urls selected!")
        else:
            print key
            self.start_urls = URL_MAP.get(key)
            print(self.start_urls)
            self.rules = RULE_MAP.get(key)
            print(self.rules)
            #select self_start_urls and self_rules based on the parameter
#        self.start_urls = ['http://www.yahoo.com']
        super(GeneralSpider, self).__init__(self, **kwargs)

#    def start_requests(self):
#        yield Request('http://www.yahoo.com', self.parse)

    def parse_content(self, response):
        depth = response.meta['depth']
        print depth
        print response.url

        item = CommonItem()
        item['link'] = response.url
        item['content'] = response.body
        return item
