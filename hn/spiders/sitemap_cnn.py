from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from hn.items import SitemapItem

## processing cnn

def process_cnn_sitemap(spider, body):
    print "Enter processing sitemap for cnn"
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
            date = news.find('news:publication_date')
            item['update'] = date.text
        
        req = Request(link, callback = spider.process_page)
        if item is not None:
            req.meta['item'] = item
        else:
            pass
        yield req


def process_cnn_page(response):
    item = response.meta.get('item')
    if item is None:
        item = SitemapItem()
#        data = bs(response.body)
#        title = data.find('h1', {"class": "title"})
#        if title is not None:
#            item['title'] = title.string
#        else:
#            pass
    else:
        pass
    item['link'] = response.url
    item['content'] = response.body
    yield item
