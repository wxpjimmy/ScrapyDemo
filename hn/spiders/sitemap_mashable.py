from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from hn.items import SitemapItem

## processing mashable

def process_mashable_sitemap(spider, body):
    print "Enter processing sitemap for mashable"
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
            #format: 2014-04-21T00:41:06Z
            date = news.find('n:publication_date')
            item['update'] = date.text
        else:
            lastmod = url.find('lastmod')
            if lastmod is not None:
                item = SitemapItem()
                #format: 2012-07-16T10:27:55Z
                item['update'] = lastmod.text
        
        req = Request(link, callback = spider.process_page)
        if item is not None:
            req.meta['item'] = item
        else:
            pass
        yield req


def process_mashable_page(response):
    #TODO: add filter here
    item = response.meta.get('item')
    if item is None:
        item = SitemapItem()
    else:
        pass
    item['link'] = response.url
    item['content'] = response.body
    yield item
