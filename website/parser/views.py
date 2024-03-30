from django.shortcuts import render
from django.http import HttpRequest

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

        found = soup.find(class_='js-product-grid-wrap')  # сетка продуктов
        if not found:
            return []
        found = found.find_all(class_='product-wrap-grid js-product-ga-wrap')  # излечение из сетки
        res = []
        for x in found:
            title = x.find(class_='product-name-grid').text
            price = float(x.find(class_='price').text.replace('€', '').replace('.', '').replace(',', '.'))
            link = x.find(class_='product-link').get('href')
            picture = x.find(id=re.compile(r'prod_pic_\d+')).get('data-src')
            res.append({'title': title.replace('\n', ''), 'price': price, 'link': link, 'picture': picture})
        res.sort(key=lambda x: x['price'])
        return [x for x in res[:MAX_ITEMS]]


def parse_datika(search_text):
    prepared_text = search_text.replace(
        " ", "+"
    )  # аргумент запроса содержит плюсы вместо пробелов
    response = requests.get(
        f"https://datika.me/search/?query={prepared_text}"
    )

    if check_200_status(response.status_code):
        soup = BeautifulSoup(response.content, "html.parser")

        found = soup.find(class_='product-list products_view_grid')  # сетка продуктов
        items = found.find_all(attrs={"itemtype":"http://schema.org/Product"})
        res = []
        if not found:
            return []
        for item in items:
            title = item.find(attrs={"itemprop": "name"}).text
            price = item.find(class_='price nowrap').text
            price = price.replace(',', '').replace(' ', '')
            price = float(re.search(r'\d+(?:\.\d+)?', price)[0])
            picture = 'https://datika.me' + item.find(attrs={"itemprop": "image"}).get('src')
            link = item.find('h5')
            link = 'https://datika.me' + link.find('a').get('href')
            res.append({'title': title, 'price': price, 'link': link, 'picture': picture})

        return res


def parse_sources(search_text: str):
    res = {}
    res['tehnomax'] = parse_tehnomax(search_text)
    res['datika'] = parse_datika(search_text)
    return res



# Create your views here.
def index(request: HttpRequest):
    if request.method == 'POST':
        search_text = request.POST.get('search_text')  # Получаем значение поля с именем 'query'
        return render(request, 'parser/index.html', context={'parsed_sources': parse_sources(search_text)})
    elif request.method == 'GET':
        return render(request, 'parser/index.html')
