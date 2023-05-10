import requests
from bs4 import BeautifulSoup
import lxml
import json
import csv

url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/110.0.0.0 "
                  "YaBrowser/23.3.3.721 "
                  "Yowser/2.5 Safari/537.36"
}


# req = requests.get(url, headers)
# src = req.text
# print(src)
#
# with open('temp/index.html', 'w', encoding="utf-8") as file:
#     file.write(src)

with open('temp/index.html', encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')
full_url = soup.find_all(class_='mzr-tc-group-item-href')
category_url = {}
for x in full_url:
    url_text = x.text
    url_x = 'https://health-diet.ru' + x.get('href')
    category_url[url_text] = url_x

