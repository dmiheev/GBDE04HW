# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import json
import requests

api_key = 'D70F0BBA0D83570D'
email = 'zzzzz@mail.ru'
file_name = f'{email}.json'

main_link = 'https://api.emailverifyapi.com/v3/lookups/json'

x_params = {
    'key': api_key,
    'email': email
}

response = requests.get(main_link, params=x_params)

if response.ok:
    j_data = response.json()
    with open(file_name, "w", encoding="utf-8") as write_f:
        json.dump(j_data, write_f, indent=4, ensure_ascii=False)
