from bs4 import BeautifulSoup as bs
from scrapy.spider import Spider
from scrapy.http import Request
from hn.items import TcNewItem
from ElasticsearchClient import ES
import re
import os
import datetime
from scrapy.utils.sitemap import Sitemap, sitemap_urls_from_robots
from scrapy.utils.gz import gunzip, is_gzipped
from sitemap_util import *


class GeneralSitemapSpider(Spider):
    name = 'sitemap'

    start_urls = []

    def __init__(self, s_type=None, **kwargs):
        if s_type is None:
            raise Exception("Must specify a spider type!")
        else:
            # load urls, load last crawled time
            





