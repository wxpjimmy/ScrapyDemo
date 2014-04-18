# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class HnItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    link = Field()


class TechCrunchItem(Item):
    link = Field()
    content = Field()


class TcNewItem(Item):
    link = Field()
    content = Field()
    update = Field()



class MSNItem(Item):
    link = Field()
    content = Field()
