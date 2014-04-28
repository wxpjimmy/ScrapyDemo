from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from hn.items import SitemapItem
import dateutil
from dateutil.parser import parse

## processing yahoo news

def process_yahoo_sitemap(spider, body):
    print "Enter processing sitemap for yahoo"
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
            #format: 2014-04-22T22:27:49+00:00
            date = news.find('news:publication_date')
            dt = parse(date.text)
            dt_utc = dt.astimezone(dateutil.tz.tzutc()).replace(tzinfo=None)
            item['update'] = dt_utc
        else:
            lastmod = url.lastmod
            if lastmod:
                item = SitemapItem()
                #format: 2014-04-23T09:14:00+00:00
                dt = parse(lastmod.text)
                dt_utc = dt.astimezone(dateutil.tz.tzutc()).replace(tzinfo=None)
                item['update'] = dt_utc
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

