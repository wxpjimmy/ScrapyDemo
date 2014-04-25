from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from hn.items import SitemapItem

## processing nytimes news

def process_nytimes_sitemap(spider, body):
    print "Enter processing sitemap for nytimes"
    data = bs(body)
    urls = data.find_all('url')
    for url in urls:
        link = url.loc.text
        item = SitemapItem()
        #format: 2014-04-23T18:32:03+00:00
        item['update'] = url.lastmod.text
        news = url.find('news:news')
        if news is not None:
            title = news.find('news:title')
            item['title'] = title.text
        
        req = Request(link, callback = spider.process_page)
        req.meta['item'] = item
        yield req


def process_nytimes_page(response):
    item = response.meta.get('item')
    item['link'] = response.url
    item['content'] = response.body
    yield item
