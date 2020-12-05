# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import json
import requests

username = 'dmiheev'
file_name = f'{username}.json'

main_link = f'https://api.github.com/users/{username}/repos'

response = requests.get(main_link)

if response.ok:
    j_data = response.json()
    with open(file_name, "w", encoding="utf-8") as write_f:
        json.dump(j_data, write_f, indent=4, ensure_ascii=False)
