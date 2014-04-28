from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


URL_MAP = { "yahoo": ["http://www.yahoo.com"],
        "gnews": ["https://news.google.com"]}


RULE_MAP = { "yahoo": (
            Rule(SgmlLinkExtractor(deny=('\.js', '\.php', 'search.yahoo.com','yahoo.uservoice.com', '\?q=')), callback='process_content', follow=True),
            ),
            "gnews":  (
            Rule(SgmlLinkExtractor(allow=(r'https?://news.google.com/news/section.*'), deny=(r'.*ict=clu_top'), restrict_xpaths=(r'//*[@id="nav-menu-wrapper"]', r'//*[@id="main-pane"]/div/div/div[3]'))),
            Rule(SgmlLinkExtractor(allow=(r'.*'), deny=(r'.*//\w+.google.*/.*', r'.js', r'.php')), callback='process_content'),
            )
            }

DONT_FILTER = {
                "gnews": [r'https?://news.google.com/news/section.*'],
                }
