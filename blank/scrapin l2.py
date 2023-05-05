from bs4 import BeautifulSoup
import json
import requests
import csv


# url = 'https://health-diet.ru/table_calorie/'
#
headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/110.0.0.0 YaBrowser/23.3.3.721 Yowser/2.5 Safari/537.36'
}
# req = requests.get(url, headers=headers)
# src = req.text
# # print(src)
#
#
# with open('index.html', 'w', encoding='utf-8') as file:
#     file.write(src)

#--------------------------------2----------------------------
# with open('index.html', encoding='utf-8') as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, 'lxml')
# all_product = soup.find_all(class_='mzr-tc-group-item-href')
# all_product_dict = {}
#
# for product in all_product:
#     prod_text = product.text
#     prod_get = 'https://health-diet.ru' + product.get('href')
#     # print(F'{prod_text}: {prod_get}')
#     all_product_dict[prod_text] = prod_get
#
# with open('all_product_dict.json', 'w', encoding='utf-8') as file:
#     json.dump(all_product_dict, file, indent=4, ensure_ascii=False)

#---------------------------------3--------------------------------

with open('all_product_dict.json', encoding='utf-8') as file:
    all_product = json.load(file)
# print(all_product)


iteration_count = int(len(all_product))-1
count = 0
print(f'Всего итераций{iteration_count}')
for category_name, all_product_href in all_product.items():

    rep = [',', ' ', '-', "'"]
    for symbol in rep:
        if symbol in category_name:
            category_name = category_name.replace(symbol, '_')

    # print(all_product_name)

    req = requests.get(url=all_product_href, headers=headers)
    src = req.text

    with open(f"date/{count}_{category_name}.html", 'w', encoding='utf-8') as file:
        file.write(src)

    with open(f"date/{count}_{category_name}.html", encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    alert_block = soup.find(class_='uk-alert-danger')
    if alert_block is not None:
        continue

    table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f'date/{count}_{category_name}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
                (
                    product,
                    calories,
                    proteins,
                    fats,
                    carbohydrates,
                )
        )

    products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

    products_info = []

    for items in products_data:
        products_tds = items.find_all('td')

        title = products_tds[0].find('a').text
        calories = products_tds[1].text
        proteins = products_tds[2].text
        fats = products_tds[3].text
        carbohydrates = products_tds[4].text

        products_info.append(
            {
                'title': title,
                'calories': calories,
                'proteins': proteins,
                'fats': fats,
                'carbohydrates': carbohydrates,
            }
        )

        with open(f'date/{count}_{category_name}.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                    (
                        title,
                        calories,
                        proteins,
                        fats,
                        carbohydrates
                    )
            )

    with open(f'date/{count}_{category_name}.json', 'a', encoding='utf-8' ) as file:
        json.dump(products_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f'# Итерация {count}.{category_name} запписан.....')
    iteration_count = iteration_count-1
    if iteration_count == 0:
        print('работа закончена')
        break
    print(f'Осталось итерацй{iteration_count}')

