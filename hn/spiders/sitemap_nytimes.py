from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from hn.items import SitemapItem
import dateutil
from dateutil.parser import parse

## processing nytimes news

def process_nytimes_sitemap(spider, body):
    print "Enter processing sitemap for nytimes"
    data = bs(body)
    urls = data.find_all('url')
    for url in urls:
        link = url.loc.text
        item = SitemapItem()
        #format: 2014-04-23T18:32:03+00:00
        dt = parse(url.lastmod.text)
        dt_utc = dt.astimezone(dateutil.tz.tzutc()).replace(tzinfo=None)
        item['update'] = dt_utc
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
