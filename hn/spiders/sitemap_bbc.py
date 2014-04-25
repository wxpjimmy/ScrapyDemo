from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from hn.items import SitemapItem
import datetime

## processing bbc

def process_bbc_sitemap(spider, body):
    print "Enter processing sitemap for bbc"
    data = bs(body)
    urls = data.find_all('url')
    for url in urls:
        link = url.loc.text
        news = url.find('news:news')
        item = None
        if news is not None:
            item = SitemapItem()
            title = news.find('news:title')
            item['title'] = title.text
            #format: 2014-04-25T09:43:49Z
            date = news.find('news:publication_date')
            item['update'] = datetime.datetime.strptime(date.text.strip(), '%Y-%m-%dT%H:%M:%SZ')

        else:
            lastmod = url.find('lastmod')
            if lastmod:
                item = SitemapItem()
                #format: 2014-04-25T10:27:05Z
                item['update'] = datetime.datetime.strptime(lastmod.text.strip(), '%Y-%m-%dT%H:%M:%SZ')

        
        req = Request(link, callback = spider.process_page)
        if item is not None:
            req.meta['item'] = item
        else:
            pass
        yield req


def process_bbc_page(response):
    item = response.meta.get('item')
    if item is None:
        item = SitemapItem()
    else:
        pass
    item['link'] = response.url
    item['content'] = response.body
    yield item

