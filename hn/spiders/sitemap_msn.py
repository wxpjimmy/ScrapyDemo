from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from hn.items import SitemapItem
import datetime

## processing msn news

def process_msn_sitemap(spider, body):
    print "Enter processing sitemap for msn"
    try:
        data = bs(body)
        urls = data.find_all('url')
        for url in urls:
            link = url.loc.text
            item = SitemapItem()
            #format: 2012-10-29T05:42:07Z
            item['update'] = datetime.datetime.strptime(url.lastmod.text.strip(), '%Y-%m-%dT%H:%M:%SZ')
            req = Request(link, callback = spider.process_page)
            req.meta['item'] = item
            yield req
    except Exception, e:
        print e

def process_msn_page(response):
    item = response.meta.get('item')
    if item is None:
        item = SitemapItem()
    else:
        pass
    item['link'] = response.url
    item['content'] = response.body
    yield item

