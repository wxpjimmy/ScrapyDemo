from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from hn.items import SitemapItem

## processing forbes

def process_forbes_sitemap(spider, body):
    print "Enter processing sitemap for forbes"
    data = bs(body)
    urls = data.find_all('url')
    for url in urls:
        link = url.loc.string
        news = url.find('news:news')
        item = None
        if news is not None:
            item = SitemapItem()
            title = news.find('news:title')
            item['title'] = title
            #date format: 2014-04-22
            date = news.find('news:publication_date')
            item['update'] = date
        
        req = Request(link, callback = spider.process_page)
        if item is not None:
            req.meta['item'] = item
        else:
            pass
        yield req


def process_forbes_page(response):
    item = response.meta.get('item')
    if item is None:
        item = SitemapItem()
    else:
        pass
    item['link'] = response.url
    item['content'] = response.body
    yield item

