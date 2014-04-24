from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from hn.items import SitemapItem

## processing ask.com

def process_huffingtonpost_sitemap(spider, body):
    print "Enter processing sitemap for ask"
    data = bs(body)
    urls = data.find_all('url')
    for url in urls:
        link = url.loc.string
        news = url.find('n:news')
        item = SitemapItem()
        #formt 2013-07-28
        item['update'] = url.lastmod
        req = Request(link, callback = spider.process_page)
        req.meta['item'] = item
        yield req



def process_huffingtonpost_page(response):
    item = response.meta.get('item')
    if item is None:
        item = SitemapItem()
    else:
        pass
    item['link'] = response.url
    item['content'] = response.body
    return item

