# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    user_id = scrapy.Field()
    profile_pic_url = scrapy.Field()
    full_name = scrapy.Field()

    subscription_id = scrapy.Field()
    subscription_username = scrapy.Field()

    subscriber_id = scrapy.Field()
    subscriber_username = scrapy.Field()

    full_data = scrapy.Field()
