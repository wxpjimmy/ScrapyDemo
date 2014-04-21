from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


URL_MAP = { "yahoo": ["http://www.yahoo.com"],
        "gnews": ["http://news.google.com"]}


RULE_MAP = { "yahoo": (
            Rule(SgmlLinkExtractor(deny=('\.js', '\.php', 'search.yahoo.com','yahoo.uservoice.com', '\?q=')), callback='parse_content', follow=True),
            ),
            "gnews": (
                Rule(SgmlLinkExtractor(restrict_xpaths=(r'//*[@id="main-pane"]')), callback='parse_content', follow=True),
                )
            }
