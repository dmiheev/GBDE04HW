"""
Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
"""
import requests
from pprint import pprint
from lxml import html

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:84.0) Gecko/20100101 Firefox/84.0'}
news_list = []

# NEWS.MAIL.RU
url = 'https://news.mail.ru/'
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

links = dom.xpath("//a[contains(@class,'js-topnews__item')]/@href")
links = links + dom.xpath("//a[@class='list__text']/@href")

for link in links:
    news = {}
    url = link
    response = requests.get(url, headers=header)
    dom = html.fromstring(response.text)
    datetime = dom.xpath("//span[contains(@class,'note__text')]/@datetime")[0]
    name = dom.xpath("//h1/text()")[0]
    source = dom.xpath("//a[contains(@class,'breadcrumbs__link')]/span/text()")[0]

    news['source'] = source
    news['name'] = name
    news['url'] = url
    news['datetime'] = datetime

    news_list.append(news)

# LENTA.RU ГЛАВНЫЕ НОВОСТИ
main_url = 'https://lenta.ru'
response = requests.get(main_url, headers=header)
dom = html.fromstring(response.text)

links = dom.xpath("//div[contains(@class,'b-yellow-box__wrap')]//a/@href")
for link in links:
    news = {}
    url = main_url + link
    response = requests.get(url, headers=header)
    dom = html.fromstring(response.text)

    name = dom.xpath("//h1/text()")[0]
    datetime = dom.xpath("//time[@class ='g-date']/@datetime")[0]

    news['source'] = 'LENTA.RU'
    news['name'] = name.replace('\xa0', ' ')
    news['url'] = url
    news['datetime'] = datetime

    news_list.append(news)

# YANDEX NEWS
url = 'https://yandex.ru/news/?utm_source=main_stripe_big'
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

news_blocks = dom.xpath("//div[contains(@class,'news-top-stories')]//article")
for block in news_blocks:
    news = {}

    name = block.xpath(".//h2/text()")[0]
    url = block.xpath(".//a/@href")[0]
    source = block.xpath(".//a/text()")[0]
    datetime = block.xpath(".//span[@class='mg-card-source__time']/text()")[0]

    news['source'] = source
    news['name'] = name
    news['url'] = url
    news['datetime'] = datetime

    news_list.append(news)


pprint(news_list)
