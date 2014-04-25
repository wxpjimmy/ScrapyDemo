from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from hn.items import SitemapItem

## processing washingtonpost

def process_washingtonpost_sitemap(spider, body):
    print "Enter processing sitemap for washingtonpost"
    data = bs(body)
    urls = data.find_all('url')
    for url in urls:
        link = url.loc.text
        news = url.find('n:news')
        item = None
        if news is not None:
            item = SitemapItem()
            title = news.find('n:title')
            item['title'] = title.text
            #format: 2014-04-23T02:56:41Z
            date = news.find('n:publication_date')
            item['update'] = date.text
        else:
            #format: 2014-04-23T02:56:41Z
            lastmod = url.find('lastmod')
            if lastmode is not None:
                item = SitemapItem()
                item['update'] = lastmod.text
        req = Request(link, callback = spider.process_page)
        if item is not None:
            req.meta['item'] = item
        else:
            pass
        yield req


def process_washingtonpost_page(response):
    item = response.meta.get('item')
    if item is None:
        item = SitemapItem()
    else:
        pass
    item['link'] = response.url
    item['content'] = response.body
    yield item

