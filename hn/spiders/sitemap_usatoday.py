from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from hn.items import SitemapItem
import dateutil
from dateutil.parser import parse

## processing usatoday

def process_usatoday_sitemap(spider, s):
    print "Enter processing sitemap for usatoday"
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
            #format: 2014-04-27T00:22:07-04:00
            date = news.find('news:publication_date')
            dt = parse(date.text)
            dt_utc = dt.astimezone(dateutil.tz.tzutc()).replace(tzinfo=None)
            item['update'] = dt_utc
        
        req = Request(link, callback = spider.process_page)
        if item is not None:
            req.meta['item'] = item
        else:
            pass
        yield req


def process_usatoday_page(response):
    item = response.meta.get('item')
    if item is None:
        item = SitemapItem()
    else:
        pass
    item['link'] = response.url
    item['content'] = response.body
    yield item

