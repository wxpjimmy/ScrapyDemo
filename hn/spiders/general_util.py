from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from hn.contrib.linkextractors.lxmllinkextract import CustomLinkExtractor


URL_MAP = { "yahoo": ["http://www.yahoo.com"],
        "gnews": ["https://news.google.com"],
        "theverge": ["http://www.theverge.com"]}


RULE_MAP = { "yahoo": (
            Rule(SgmlLinkExtractor(deny=('\.js', '\.php', 'search.yahoo.com','yahoo.uservoice.com', '\?q=')), callback='process_content', follow=True),
            ),
            "gnews":  (
            Rule(SgmlLinkExtractor(allow=(r'https?://news.google.com/news/section.*'), deny=(r'.*ict=clu_top'), restrict_xpaths=(r'//*[@id="nav-menu-wrapper"]', r'//*[@id="main-pane"]/div/div/div[3]'))),
            Rule(SgmlLinkExtractor(allow=(r'.*'), deny=(r'.*//\w+.google.*/.*', r'.js', r'.php')), callback='process_content'),
            ),
            "theverge": (
            Rule(CustomLinkExtractor(allow=(r'http://www.theverge.com/\d{4}/\d{1,2}/\d{1,2}/.*')), callback='process_content'),
            Rule(CustomLinkExtractor(allow=(r'http://www.theverge.com/\w+$', r'http://www.theverge.com/us-world$'), 
                deny=(r'http://www.theverge.com/.*/.*', r'/search', r'/forums', r'/longform', r'video', r'/jobs', r'/archives'))),
#            Rule(SgmlLinkExtractor(allow=(r'/.*/archives$', r'/.*/archives/\d+$'))),
            )
            }

DONT_FILTER = {
                "gnews": [r'https?://news.google.com/news/section.*'],
                "theverge": [r'http://www.theverge.com/\w+$', r'http://www.theverge.com/us-world$']
                }
