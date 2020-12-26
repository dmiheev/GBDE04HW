# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def str_to_float(value):
    try:
        return float(value.replace('\xa0', '').replace(' ', ''))
    except Exception as e:
        print("!!!Ошибка в str_to_float", e)
        return None


def str_to_int(value):
    try:
        return int(value.replace('\xa0', '').replace(' ', ''))
    except Exception as e:
        print("!!!Ошибка в str_to_int", e)
        return None


def parse_dict(value):
    if value:
        res = {}
        dict_items = value.items()
        for i in dict_items:
            a = i[0]
            if i[1].isnumeric():
                b = int(i[1])
            else:
                try:
                    b = float(i[1])
                except:
                    b = i[1]
            res[a] = b
        return res


def process_photos(photo):
    try:
        photo = photo.replace('w_82,h_82', 'w_2000,h_2000')
        return photo
    except Exception as e:
        print("!!!Ошибка в process_photos", e)
        return photo


class LeruaItem(scrapy.Item):
    _id = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(str_to_int))
    url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(str_to_float))
    def_list = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(parse_dict))
    photos = scrapy.Field(input_processor=MapCompose(process_photos))
