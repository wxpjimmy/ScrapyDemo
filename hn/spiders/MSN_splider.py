from bs4 import BeautifulSoup as bs
from hn.items import MSNItem
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class MSNSpider(CrawlSpider):
    name='msn'
#    allowed_domains = []
    start_urls = ['http://news.msn.com']

    rules = (
            Rule(SgmlLinkExtractor(allow=(r'/.*/$'), deny=(r'/videos/'), restrict_xpaths=(r'//*[@id="nav"]'))),
            Rule(SgmlLinkExtractor(allow=('.*'), restrict_xpaths=(r'//*[@id="main"]')), callback='parse_detail'),
            )

    def parse_detail(self, response):
        self.log("parse detail: %s" % response.url)

        url = response.url
        body = response.body
        item = MSNItem()
        item['link'] = url
        item['content'] = body
        yield item

