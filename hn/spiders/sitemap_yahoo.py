from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from hn.items import SitemapItem

## processing yahoo news

def process_yahoo_sitemap(spider, body):
    print "Enter processing sitemap for yahoo"
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
            #format: 2014-04-22T22:27:49+00:00
            date = news.find('news:publication_date')
            item['update'] = date
        else:
            lastmod = url.lastmod
            if lastmod:
                item = SitemapItem()
                #format: 2014-04-23T09:14:00+00:00
                item['update'] = lastmod.string
        req = Request(link, callback = spider.process_page)
        if item is not None:
            req.meta['item'] = item
        else:
            pass
        yield req


def process_yahoo_page(response):
    item = response.meta.get('item')
    if item is None:
        item = SitemapItem()
    else:
        pass
    item['link'] = response.url
    item['content'] = response.body
    yield item

