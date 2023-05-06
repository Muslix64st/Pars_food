import requests
from bs4 import BeautifulSoup
import lxml
import json
import csv

url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

""" Применяем хедерсы что сайт не воспрнимал нас как бота  """
headers = {
    'accept': '*/*',
   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/110.0.0.0 '
                 'YaBrowser/23.3.3.721 '
                 'Yowser/2.5 '
                 'Safari/537.36',
}

# req = requests.get(url, headers)
# src = req.text
#
# with open('index_food.html', 'a', encoding='utf-8') as file:
#     file.write(src)
#
#
# soup = BeautifulSoup(src, 'lxml')
# all_categories_dict = {}
# all_products_href = soup.find_all(class_="mzr-tc-group-item-href")
# for item in all_products_href:
#     item_text = item.text
#     item_href = 'https://health-diet.ru' + item.get('href')
#     print(f'{item_text} : https://health-diet.ru{item_href}')
#
#     all_categories_dict[item_text] = item_href
#
# with open('all_categories_dict.json', 'w', encoding='utf-8') as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

#_________________________________________________

with open('all_categories_dict.json', encoding='utf-8') as file:
    all_categories = json.load(file)

all_poduct_dict = {}
full_product_dict = {}
count2 = 0
count = 0
for category_name, category_href in all_categories.items():
    if count == 0:
        rep = [',', '-', '.', '\'']
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, '_')

            req = requests.get(url=category_href, headers=headers)
            src = req.text

            with open(f'data/{count}{category_name}.html', 'w', encoding='utf-8') as file:
                file.write(src)


            with open(f'data/{count}{category_name}.html', encoding='utf-8') as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')

            table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
            product = table_head[0].text
            colories = table_head[1].text
            proteins = table_head[2].text
            fast = table_head[3].text
            carbohydrates = table_head[4].text

            product_data = soup.find(class_="mzr-tc-group-table").find('tbody').find_all('tr')
            for item in product_data:
                product_tds = item.find_all('td')
                product_href = item.find_all('a')
                title = product_tds[0].find('a').text
                full_product_dict[title] = product_href

            product_name_url = soup.find(class_="mzr-tc-group-table").find('tbody').find_all('a')
            for x in product_name_url:
                x_href = 'https://health-diet.ru' + x.get('href')
                x_title = x.text
                full_product_dict[x_title] = x_href

            with open('product_dict.json', 'w', encoding='utf-8') as file:
                json.dump(full_product_dict, file, indent=4, ensure_ascii=False)

            # with open('product_dict.json', encoding='utf-8') as file:
            #     full_product = json.load(file)
            #
            # for product_name, product_href in full_product.items():
            #     if count2 == 0:
            #         rep = [',', '-', '.', '\'']
            #         for item in rep:
            #             if item in category_name:
            #                 category_name = category_name.replace(item, '_')
            #
            #             req = requests.get(url=product_href, headers=headers)
            #             src = req.text
            #
            #             with open(f'data/{count}{product_name}.html', 'w', encoding='utf-8') as file:
            #                 file.write(src)
            #
            #             with open(f'data/{count}{product_name}.html', encoding='utf-8') as file:
            #                 src = file.read()
            #
            #             soup = BeautifulSoup(src, 'lxml')
            #             table_head = soup.find(class_='el-table').find('tbody').find('tr').find_all('td')
            #             # product_rsp = table_head[0].text
            #             # colories = table_head[1].text
            #             # proteins = table_head[2].text
            #             # fast = table_head[3].text
            #             # carbohydrates = table_head[4].text
            #             print(table_head[0])
            #             count2 += 1
    count += 1

with open('product_dict.json', encoding='utf-8') as file:
    full_product = json.load(file)

for product_name, product_href in full_product.items():
    if count2 == 0:
        rep = [',', '-', '.', '\'']
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, '_')

            req = requests.get(url=product_href, headers=headers)
            src = req.text

            with open(f'data/{count}{product_name}.html', 'w', encoding='utf-8') as file:
                file.write(src)

            with open(f'data/{count}{product_name}.html', encoding='utf-8') as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')
            table_head = soup.find(class_='mzr-nutrition-value').find('tbody').find_all('tr')#.find_all('td')
            for item in table_head:
                product_tds = item.find_all('td')
                # product_href = item.find_all('a')
                # title = product_tds[0].find('a').text
                # full_product_dict[title] = product_href

            table_head = soup.find(class_='mzr-nutrition-value').find('tbody').find_all('tr')
            product = table_head[0]
            colories = table_head[1]
            proteins = table_head[2]
            fast = table_head[3]
            # carbohydrates = table_head[4].text
            print(product, colories, proteins, fast)


            count2 += 1