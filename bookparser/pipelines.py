# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books_db

    def process_item(self, item, spider):
        item['old_price'] = self.process_old_price(spider.name, item['old_price'])
        item['price'] = self.process_price(item['price'])
        item['rating'] = self.process_rating(item['rating'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_old_price(self, spider_name, old_price):
        if old_price:
            if spider_name == 'books24ru':
                try:
                    list = old_price.split()
                    a = list.pop(-1)  # отрезаем р.
                    res = "".join(list)
                    res = float(res)
                except Exception as e:
                    print('Ошибка в process_old_price: ', e)
                    res = f'!!!{old_price}'
                return res
            elif spider_name == 'labirint':
                try:
                    return float(old_price)
                except Exception as e:
                    print('Ошибка в process_old_price: ', e)
                    return f'!!!{old_price}'
        else:
            return None

    def process_price(self, price):
        if price:
            try:
                res = price.replace(' ', '').replace('\xa0', '')
                res = float(res)
            except Exception as e:
                print('Ошибка в process_price: ', e)
                res = f'!!!{price}'
            return res
        else:
            return None

    def process_rating(self, rating):
        if rating:
            try:
                return float(rating.replace(',', '.'))
            except Exception as e:
                print('Ошибка в process_rating: ', e)
                return f'!!!{rating}'
        else:
            return None
