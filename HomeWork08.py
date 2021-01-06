"""
4) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
5) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь
"""
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)

db = client['instaparser']
instaparser = db.instagram

search_for = 'netjet88'

for subscriber in instaparser.find({'subscription_username': search_for}, {'_id': 0, 'full_data': 0}):
    pprint(subscriber)

for subscription in instaparser.find({'subscriber_username': search_for}, {'_id': 0, 'full_data': 0}):
    pprint(subscription)
