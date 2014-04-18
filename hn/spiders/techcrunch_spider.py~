from bs4 import BeautifulSoup as bs
from scrapy.contrib.spiders import SitemapSpider
from scrapy.http import Request
from hn.items import TechCrunchItem
from ElasticsearchClient import ES

class TechCrunchSpider(SitemapSpider):
    name = 'tc'
    es = ES({"localhost":9200}, 'techcrunch', 'perf')

    sitemap_urls = ['http://techcrunch.com/sitemap.xml']

    sitemap_rules = [('.*yyyy=\d{4}&mm=\d{2}&dd=\d{2}', 'parse_eachday'),
            ('.*/\d{4}/\d{2}/\d{2}/.*', 'parse_content'),
            ('.*/tag/.*', 'parse_content')]
#            ('.*', 'parse_page')]

    def parse_eachday(self, response):
        url = response.url
        print "Parse root level page"
        return Request(url, callback=self.parse_content)

    def parse_content(self, response):
        url = response.url
        data = response.body
        tc_item = TechCrunchItem()
        tc_item['link'] = url
        tc_item['content'] = data
        self.es.index(url, data)
        print("Finished download url: %s, len: %d" % (url, len(data)))

        yield tc_item
