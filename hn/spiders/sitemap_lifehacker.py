from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from hn.items import SitemapItem
import dateutil
from dateutil.parser import parse

## processing lifehacker

def process_lifehacker_sitemap(spider, body):
    print "Enter processing sitemap for lifehacker"
    data = bs(body)
    urls = data.find_all('url')
    for url in urls:
        link = url.loc.text
        if link.trip() == 'http://lifehacker.com':
            continue
        else:
            item = SitemapItem()
            #format: 2014-04-18T11:30:00-07:00
            dt = parse(url.lastmod.text)
            dt_utc = dt.astimezone(dateutil.tz.tzutc()).replace(tzinfo=None)
            item['update'] = dt_utc
            req = Request(link, callback = spider.process_page)
            if item is not None:
                req.meta['item'] = item
            else:
                pass
            yield req


def process_lifehacker_page(response):
    item = response.meta.get('item')
    if item is None:
        item = SitemapItem()
    else:
        pass
    item['link'] = response.url
    item['content'] = response.body
    yield item


