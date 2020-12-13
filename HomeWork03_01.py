# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB
# и реализовать функцию, записывающую собранные вакансии в созданную БД.
# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.

from pymongo import MongoClient
import get_hh_data as hh
import get_sj_data as sj
from pprint import pprint


def filter_salary(x_sal):
    """2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше
    введённой суммы. Поиск должен происходить по 2-ум полям (минимальной и максимальной зарплате)"""
    conditions = {'$or': [{'$and': [{'salary min': None}, {'salary max': {'$gte': x_sal}}]},
                          {'$and': [{'salary max': None}, {'salary min': {'$lte': x_sal}}]},
                          {'$and': [{'salary max': {'$gte': x_sal}}, {'salary min': {'$lte': x_sal}}]}]}

    for f in hh_db.find(conditions):
        pprint(f)
    for f in sj_db.find(conditions):
        pprint(f)


conn = MongoClient('127.0.0.1', 27017)
db = conn['vacancy_db']
hh_db = db.hh_db
sj_db = db.sj_db

# HeadHunter
vacancy_list = hh.get_hh_data('python', 1)
for vacancy in vacancy_list:
    vacancy_id = vacancy['vacancy_id']
    # Если вакансии не существует в базе, то добавим её
    if hh_db.count_documents({'vacancy_id': vacancy_id}) == 0:
        hh_db.insert_one(vacancy)

# SuperJob
vacancy_list = sj.get_sj_data('python', 1)
for vacancy in vacancy_list:
    vacancy_id = vacancy['vacancy_id']
    # Если вакансии не существует в базе, то добавим её
    if sj_db.count_documents({'vacancy_id': vacancy_id}) == 0:
        sj_db.insert_one(vacancy)

# Фильтр по ЗП... не обрабатывается валюта
filter_salary(100000)
