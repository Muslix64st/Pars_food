import random
from time import sleep

import requests
from bs4 import BeautifulSoup
import lxml
import json
import csv

# url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"
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

# ____________________________________________________________________
# with open('temp/index.html', encoding="utf-8") as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, 'lxml')
# full_url = soup.find_all(class_='mzr-tc-group-item-href')
# category_url = {}
# for x in full_url:
#     url_text = x.text
#     url_x = 'https://health-diet.ru' + x.get('href')
#     category_url[url_text] = url_x
#
# with open('temp/cat_url.json', 'w', encoding="utf-8") as file:
#     json.dump(category_url, file, indent=4, ensure_ascii=False)

# _____________________________________________________________________
#
with open('temp/cat_url.json', encoding="utf-8") as file:
    all_cat = json.load(file)

iteration_count = int(len(all_cat)) - 1
print(f'Всего итераций: {iteration_count}')

count = 0

for cat_name, cat_url in all_cat.items():
    req = requests.get(url=cat_url, headers=headers)
    src = req.text

    with open(f'data/table_HTML/{count}_{cat_name}.html', 'w', encoding="utf-8") as file:
        file.write(src)

    with open(f'data/table_HTML/{count}_{cat_name}.html', encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    alert_block = soup.find(class_='uk-alert-danger')

    if alert_block is not None:
        continue

    table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    # for i in range(len(table_head)):
    #     print(table_head[i].text)
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fast = table_head[3].text
    carbohydrates = table_head[4].text
    print(product, calories, proteins, fast, carbohydrates)  # Продукт Калорийность Белки Жиры Углеводы

    with open(f'data/table_CSV/{count}_{cat_name}.csv', 'w', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fast,
                carbohydrates,
            )
        )
    product_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

    prod_info = []

    for x in product_data:
        product_url = x.find_all('td')
        title = product_url[0].find('a').text
        calories = product_url[1].text
        proteins = product_url[2].text
        fast = product_url[3].text
        carbohydrates = product_url[4].text

        prod_info.append(
            {
                'title': title,
                'calories': calories,
                'proteins': proteins,
                'fast': fast,
                'carbohydrates': carbohydrates
            }
        )

        with open(f'data/table_CSV/{count}_{cat_name}.csv', 'a', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fast,
                    carbohydrates
                )
            )

    count += 1

    with open(f'data/table_JSON/{count}_{cat_name}.json', 'a', encoding="utf-8") as file:
        json.dump(prod_info, file, indent=4, ensure_ascii=False)


    print(f"# Итерация {count}. {cat_name}  прошла успешно")
    iteration_count -= 1
    if iteration_count == 0:
        print('ГОТОВО')
        break
    else:
        print(f'Осталось {iteration_count} итераций')
    sleep(random.randrange(0, 3))