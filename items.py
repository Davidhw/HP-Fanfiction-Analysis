# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class HpfanficItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    author = Field()
    desc = Field()	
    other_info = Field()
    chapters = Field()
    rating = Field()
    language = Field()
    genre = Field()
    words = Field()
    reviews = Field()
    favorites = Field()
    follows = Field()
    updated = Field()
    published = Field()
    staringchars = Field()
    complete = Field()
    pass







