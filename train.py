from bs4 import BeautifulSoup
import requests
import re

MAX_ITEMS = 10


def handle_data(parsed_data: list, source: str):
    if parsed_data:
        for i, x in enumerate(parsed_data):
            print('-' * 15 + f'ITEM {i + 1}' + '-' * 15 + '\n', x)
    else:
        print(f'Нет данных. Источник "{source}"')


def check_200_status(value: int):
    if value == 200:
        return True
    print("Ошибка при получении страницы:", value)
    return False


def parse_tehnomax(search_text):
    prepared_text = search_text.replace(
        " ", "+"
    )  # аргумент запроса содержит плюсы вместо пробелов
    response = requests.get(
        f"https://www.tehnomax.me/index.php?mod=catalog&op=thm_search&search_type=&submited=1&keywords={prepared_text}"
    )

    if check_200_status(response.status_code):
        soup = BeautifulSoup(response.content, "html.parser")

        found = soup.find(class_='js-product-grid-wrap') # сетка продуктов
        if not found:
            return []
        found = found.find_all(class_='product-wrap-grid js-product-ga-wrap') # излечение из сетки
        res = []
        for x in found:
            title = x.find(class_='product-name-grid').text
            price = float(x.find(class_='price').text.replace('€', '').replace('.', '').replace(',', '.'))
            link = x.find(class_='product-link').get('href')
            picture = x.find(id=re.compile(r'prod_pic_\d+')).get('data-src')
            res.append({'title': title.replace('\n', ''), 'price': price, 'link': link, 'picture': picture})
        res.sort(key=lambda x: x['price'])
        return [x for x in res[:MAX_ITEMS]]


search_text = 'VES MASINA LG PROFI 10 KG'
parsed_data = parse_tehnomax(search_text)
handle_data(parsed_data, "tehnomax")
