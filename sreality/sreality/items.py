# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class SRealityItem(scrapy.Item):
    title = scrapy.Field()
    image_url = scrapy.Field()
