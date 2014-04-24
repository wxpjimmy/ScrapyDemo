from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from hn.items import CommonItem

class GoogleNewsSpider(CrawlSpider):
    name='gnews'

    start_urls = ["http://news.google.com"]

    rules = (
            Rule(SgmlLinkExtractor(allow=(r'https?://news.google.com/news/section.*'), deny=(r'.*ict=clu_top'), restrict_xpaths=(r'//*[@id="nav-menu-wrapper"]', r'//*[@id="main-pane"]/div/div/div[3]'))),
            Rule(SgmlLinkExtractor(allow=(r'.*'), deny=(r'.*//\w+.google.com/.*', r'.js', r'.php')), callback='process_content'),
            )

    def __init__(self, **kwargs):
       super(GoogleNewsSpider, self).__init__(self.name, **kwargs)

    def process_content(self, response):
        print "Entering process content..."
        print response.url
        try:
            item = CommonItem()
            item['link'] = response.url
#        item['content'] = response.body
            return item
        except Exception, e:
            print e

    def __str__(self):
        return self.name

