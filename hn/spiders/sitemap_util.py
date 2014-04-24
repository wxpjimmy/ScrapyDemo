from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from hn.items import SitemapItem
from sitemap_wsj import *
from sitemap_cnn import *
from sitemap_reuter import *
from sitemap_bbc import *
from sitemap_forbes import *
from sitemap_usatoday import *
from sitemap_lifehacker import *
from sitemap_mashable import *
from sitemap_washingtonpost import *

from sitemap_yahoo import *
from sitemap_msn import *
from sitemap_nytimes import *


## processing huffingtonpost

def process_huffingtonpost_sitemap(spider, body):
    print "Enter processing sitemap for huff"
    data = bs(body)
    urls = data.find_all('url')
    for url in urls:
        link = url.loc.string
        news = url.find('n:news')
        item = None
        if news is not None:
            item = SitemapItem()
            title = news.find('n:title')
            item['title'] = title
            date = news.find('n:publication_date')
            item['update'] = date
        
        req = Request(link, callback = spider.process_page)
        if item is not None:
            req.meta['item'] = item
        else:
            pass
        yield req


def process_huffingtonpost_page(response):
    item = response.meta.get('item')
    if item is None:
        item = SitemapItem()
        data = bs(response.body)
        title = data.find('h1', {"class": "title"})
        if title is not None:
            item['title'] = title.string
        else:
            pass
    else:
        pass
    item['link'] = response.url
    item['content'] = response.body
    yield item



SM_FUNC = { "huff": process_huffingtonpost_sitemap,
            "wsj": process_wsj_sitemap,
            "cnn": process_cnn_sitemap,
            "reuter": process_reuter_sitemap,
            "bbc": process_bbc_sitemap,
            "forbes": process_forbes_sitemap,
            "usatoday": process_usatoday_sitemap,
            "lifehacker": process_lifehacker_sitemap,
            "mashable": process_mashable_sitemap,
            "washingtonpost": process_washingtonpost_sitemap,
            "yahoo": process_yahoo_sitemap,
            "msn": process_msn_sitemap,
            "nytimes": process_nytimes_sitemap}

PAGE_FUNC = { "huff": process_huffingtonpost_page,
              "wsj": process_wsj_page,
              "cnn": process_cnn_page,
              "reuter": process_reuter_page,
              "bbc": process_bbc_page,
              "forbes": process_forbes_page,
              "usatoday": process_usatoday_page,
              "lifehacker": process_lifehacker_page,
              "mashable": process_mashable_page,
              "washingtonpost": process_washingtonpost_page,
              "yahoo": process_yahoo_page,
              "msn": process_msn_page,
              "nytimes": process_nytimes_page}

SM_URL = { 
        "huff": ['http://www.huffingtonpost.com/sitemap-index.xml'],
        "wsj": ['http://online.wsj.com/x_google_news.html', 
                'http://online.wsj.com/x_google_news_ap.html',
                'http://online.wsj.com/x_google_news_wire.html',
                'http://online.wsj.com/sitemap.xml',
                'http://online.wsj.com/public/resources/documents/google/wsj/google_sitemap_index.xml'],
        "cnn": ['http://edition.cnn.com/sitemaps/sitemap-news.xml',
                'http://edition.cnn.com/sitemaps/sitemap-index.xml'],
        "reuter": ['http://www.reuters.com/sitemap_news_index.xml'],
        "bbc": ['http://www.bbc.co.uk/news/news_sitemap.xml',
                'http://www.bbc.co.uk/news/sitemap.xml'],
        "forbes": ['http://www.forbes.com/news_sitemap.xml'],
        "usatoday": ['http://www.usatoday.com/news_sitemap_index.xml'],
        "lifehacker": ['http://lifehacker.com/robots.txt'],
        "mashable": ['http://mashable.com/sitemap-news.xmlo',
                     'http://mashable.com/sitemap-posts-2.xml',
                     'http://mashable.com/sitemap-posts-1.xml'],
        "ask": ['http://www.ask.com/robots.txt'],
        "washingtonpost": ['http://www.washingtonpost.com/news-sitemap-index.xml',
                           'http://www.washingtonpost.com/web-sitemap-index.xml'],
        "abcnews": ['http://abcnews.go.com/xmlLatestStories'],
        "yahoo": ['http://news.yahoo.com/sitemap/stories/index.xml',
                  'http://news.yahoo.com/sitemap/original/index.xml',
                  'http://news.yahoo.com/_s/sitemap-story.xml'],
        "msn": ['http://news.msn.com/robots.txt'],
        "nytimes": ['http://www.nytimes.com/sitemaps/sitemap_news/sitemap.xml.gz']
        }

SM_FILTER = {"cnn": ['.*/sitemap-specials-.*', '.*/sitemap-gallery-.*'],
            "msn": ['.*/photos/.*', '.*/videos/.*']}
