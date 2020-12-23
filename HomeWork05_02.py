"""
2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pprint import pprint
import time
import json

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get('https://www.mvideo.ru/')
goods_list = []


try:
    bestsellers = driver.find_element_by_xpath('//div[contains(text(),"Хиты продаж")]/ancestor::div[@class="section"]')
except Exception as e:
    print('Хиты продаж отсутствуют', e)

while True:
    cnt = 0
    try:
        goods = bestsellers.find_elements_by_xpath(".//a[@class='fl-product-tile-picture "
                                                   "fl-product-tile-picture__link']")
        for good in goods:
            g = good.get_attribute('data-product-info')
            g = g.replace('\t', '')
            g = g.replace('\n', '')
            g = json.loads(g)
            g.pop('Location')
            g.pop('eventPosition')
            if g not in goods_list:
                goods_list.append(g)
            else:
                cnt += 1
    except Exception as e:
        print('Ошибка', e)
    # крутим колесо пока добавляются новые записи
    if cnt == len(goods_list):
        break
    else:
        try:
            next_button = WebDriverWait(bestsellers, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, './/a[contains(@class,"next-btn")]')
                )
            )
            next_button.click()
            time.sleep(2)
        except Exception as e:
            print('Ошибка ', e)


pprint(goods_list)
print(f'Количество товаров: {len(goods_list)}')
driver.close()
