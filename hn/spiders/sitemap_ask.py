from scrapy.http import Request
from hn.items import SitemapItem
import datetime

## processing ask.com

def process_ask_sitemap(spider, s):
    print "Enter processing sitemap for ask"
    for values in s:
        link = values['loc']
        title = values.get('title')
        if title:
            date = values.get('publication_date')
            item = SitemapItem()
            item['title'] = title
            item['update'] = datetime.datetime.strptime(date, '%Y-%m-%d')
        else:
            #format 2014-04-27
            date = values.get('lastmod')
            if date:
                item = SitemapItem()
                item['update'] = datetime.datetime.strptime(date, '%Y-%m-%d')

        req = Request(link, callback = spider.process_page)
        if item:
            req.meta['item'] = item
        yield req



def process_ask_page(response):
    item = response.meta.get('item')
    if item is None:
        item = SitemapItem()
    else:
        pass
    item['link'] = response.url
    item['content'] = response.body
    return item

