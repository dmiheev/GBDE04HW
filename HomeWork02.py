# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы)
# с сайтов Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input
# или аргументы). Получившийся список должен содержать в себе минимум:
# * Наименование вакансии.
# * Предлагаемую зарплату (отдельно минимальную, максимальную и валюту).
# * Ссылку на саму вакансию.
# * Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести
# с помощью dataFrame через pandas.
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint


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
        return result_list
    except AttributeError:
        return [None, None, None]


def parse_salary_sj(x):
    result_list = [None, None, None]
    try:
        x = x.replace(u'\xa0', u'')
        if x == 'По договорённости' or x == 'Вакансия дня':
            return [None, None, None]
        x = x.replace('от', 'от ')
        x = x.replace('до', 'до ')
        x = x.replace('руб.', ' руб.')
        x = x.replace('USD', ' USD')
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
            if str(x_list[0]).find('—') > 0:
                result_list[0] = x_list[0].split('—')[0]
                result_list[1] = x_list[0].split('—')[1]
            else:
                result_list[0] = x_list[0]
                result_list[1] = x_list[0]
        return result_list
    except AttributeError:
        return [None, None, None]
    except IndexError:
        print(f'Ошибка в parse_salary_sj: x = {x}')
        return [None, None, None]


find = input('Найти: ')
max_pages = int(input('Введите число страниц сайта для обработки, \n0 - ВСЕ СТРАНИЦЫ: '))
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

            vacancy_data['name'] = vacancy_name.text
            vacancy_data['site'] = main_link
            vacancy_data['link'] = vacancy_link
            vacancy_data['salary min'] = vacancy_salary[0]
            vacancy_data['salary max'] = vacancy_salary[1]
            vacancy_data['salary val'] = vacancy_salary[2]

            vacancies.append(vacancy_data)

        if page_cnt == max_pages:
            break
        # Если кнопка Далее есть то ищем далее
        try:
            link = main_link + soup.find('a', {'class': 'HH-Pager-Controls-Next'})['href']
        except TypeError:
            break

main_link = 'https://www.superjob.ru'
x_params = {
    'keywords': find,
    'noGeo': '1'}
link = main_link + '/vacancy/search'
page_cnt = 0
while True:
    response = requests.get(link, params=x_params, headers=headers)
    if response.ok:
        page_cnt = page_cnt + 1
        soup = bs(response.text, 'html.parser')
        vacancy_list = soup.findAll('div', {'class': 'f-test-vacancy-item'})
        for vacancy in vacancy_list:
            vacancy_data = {}
            vacancy_name = vacancy.find('a', {'class': '_6AfZ9'})
            vacancy_link = main_link + vacancy_name['href']
            try:
                vacancy_salary = parse_salary_sj(vacancy.find('span',
                                                              {'class': '_3mfro'}).text)
            except AttributeError:
                vacancy_salary = [None, None, None]

            vacancy_data['name'] = vacancy_name.text
            vacancy_data['site'] = main_link
            vacancy_data['link'] = vacancy_link
            vacancy_data['salary min'] = vacancy_salary[0]
            vacancy_data['salary max'] = vacancy_salary[1]
            vacancy_data['salary val'] = vacancy_salary[2]

            vacancies.append(vacancy_data)

        if page_cnt == max_pages:
            break
        # Если кнопка Далее есть то ищем далее
        try:
            link = main_link + soup.find('a', {'rel': 'next'})['href']
        except TypeError:
            break

pprint(vacancies)
print(f'Вакансий обработано: {len(vacancies)}')
