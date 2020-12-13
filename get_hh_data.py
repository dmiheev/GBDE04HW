from bs4 import BeautifulSoup as bs
import requests
import json
from pprint import pprint


def get_hh_data(x_find, x_pages):
    """
    :param x_find: поисковый запрос
    :param x_pages: количество страниц для выгрузки, 0 полная выгрузка
    :return:
    """

    def parse_salary_hh(x):
        result_list = [None, None, None]
        try:
            x = x.replace(u'\xa0', u'')
            x_list = x.split()
            # парсинг валюты, 1 значение с конца
            if x_list[-1] == 'руб.':
                result_list[2] = 'RUB'
            else:
                result_list[2] = x_list[-1]
            # диапазон суммы
            if x_list[0] == 'от':
                result_list[0] = x_list[1]
                result_list[1] = None
            elif x_list[0] == 'до':
                result_list[0] = None
                result_list[1] = x_list[1]
            else:
                result_list[0] = x_list[0].split('-')[0]
                result_list[1] = x_list[0].split('-')[1]
            if result_list[0]:
                result_list[0] = int(result_list[0])
            if result_list[1]:
                result_list[1] = int(result_list[1])
            return result_list
        except AttributeError:
            return [None, None, None]

    find = x_find
    max_pages = x_pages
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:84.0) Gecko/20100101 Firefox/84.0'}
    vacancies = []

    main_link = 'https://hh.ru'
    x_params = {
        'L_save_area': 'true',
        'clusters': 'true',
        'enable_snippets': 'true',
        'text': find,
        'showClusters': 'true'}
    link = main_link + '/search/vacancy'
    page_cnt = 0
    while True:
        response = requests.get(link, params=x_params, headers=headers)
        if response.ok:
            page_cnt = page_cnt + 1
            soup = bs(response.text, 'html.parser')
            vacancy_list = soup.findAll('div', {'data-qa': 'vacancy-serp__vacancy'})
            for vacancy in vacancy_list:
                vacancy_data = {}
                vacancy_name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
                vacancy_link = vacancy_name['href']
                try:
                    vacancy_salary = parse_salary_hh(vacancy.find('span',
                                                                  {'data-qa': 'vacancy-serp__vacancy-compensation'}).text)
                except AttributeError:
                    vacancy_salary = [None, None, None]

                vacancy_id = int(json.loads(vacancy.find('script',
                                                     {'data-name': 'HH/VacancyResponsePopup/VacancyResponsePopup'}
                                                     )['data-params'])['vacancyId'])

                vacancy_data['name'] = vacancy_name.text
                vacancy_data['site'] = main_link
                vacancy_data['link'] = vacancy_link
                vacancy_data['salary min'] = vacancy_salary[0]
                vacancy_data['salary max'] = vacancy_salary[1]
                vacancy_data['salary val'] = vacancy_salary[2]
                vacancy_data['vacancy_id'] = vacancy_id

                vacancies.append(vacancy_data)

            if page_cnt == max_pages:
                break
            # Если кнопка Далее есть то ищем далее
            try:
                link = main_link + soup.find('a', {'class': 'HH-Pager-Controls-Next'})['href']
            except TypeError:
                break
    return vacancies
