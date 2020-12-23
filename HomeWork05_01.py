"""
1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pprint import pprint
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get('https://account.mail.ru/')

elem = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'username'))
       )
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)
#time.sleep(1)

elem = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'password'))
       )
elem.send_keys('NextPassword172')
elem.send_keys(Keys.ENTER)
#time.sleep(1)

first_mail = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'llc__container'))
       )
#time.sleep(1)

if first_mail:
    first_mail.click()

    mails_list = []
    cnt = 0
    while True:
        time.sleep(1)
        mail = {}
        contact = driver.find_element_by_xpath('//div[@class="letter__author"]/span').get_attribute('title')
        date = driver.find_element_by_xpath('//div[@class="letter__date"]').text
        header = driver.find_element_by_xpath('//h2').text
        body = driver.find_element_by_xpath('//div[@class="letter__body"]').text

        mail['contact'] = contact
        mail['date'] = date
        mail['header'] = header
        mail['body'] = body

        mails_list.append(mail)
        cnt += 1

        try:
            driver.find_element_by_xpath("//span[contains(@class,'button2_arrow-down')]").click()
        except Exception:
            break

    pprint(mails_list)
    pprint(f'Обработано писем: {cnt}')
    driver.close()
