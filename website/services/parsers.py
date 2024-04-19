from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from urllib.parse import quote
import re

from django.shortcuts import render
from django.http import HttpRequest
from services.utils import MulticomEncoder
from services.categories import CATEGORIES

MAX_ITEMS = 40


def check_200_status(value: int):
    if value == 200:
        return True
    print("Ошибка при получении страницы:", value)
    return False


def parse_tehnomax(search_text, category: str = None):
    response = None
    if category:
        response = requests.get(
            f'https://www.tehnomax.me/index.php?mod=catalog&op=thm_search&search_type=products&submited=1&keywords={quote(search_text)}&filters[category]={CATEGORIES[category]["tehnomax"]}&filters[promo]=&filters[stock]=dostupno',
            headers={'User-Agent': UserAgent().random}
        )
    else:
        prepared_text = search_text.replace(
            " ", "+"
        )  # аргумент запроса содержит плюсы вместо пробелов
        response = requests.get(
            f'https://www.tehnomax.me/index.php?mod=catalog&op=thm_search&search_type=&submited=1&keywords={prepared_text}',
            headers={'User-Agent': UserAgent().random}
        )

    if check_200_status(response.status_code):
        soup = BeautifulSoup(response.content, "html.parser")

        found = soup.find_all(class_='product-wrap-grid js-product-ga-wrap')
        if not found:
            return []
        res = []
        for x in found:
            title = x.find(class_='product-name-grid')
            if title:
                title = title.text
                if title.lower().find(search_text.lower()) == -1:
                    continue
            else:
                continue
            price = x.find(class_='price')
            if price:
                price = float(price.text.replace('€', '').replace('.', '').replace(',', '.'))
            else:
                continue
            link = x.find(class_='product-link').get('href')
            picture = x.find(id=re.compile(r'prod_pic_\d+')).get('data-src')
            res.append({'title': title.replace('\n', ''), 'price': price, 'link': link, 'picture': picture})
        res.sort(key=lambda x: x['price'])
        return res


def parse_datika(search_text, category: str = None):
    if category:
        response = requests.get(
            f'',
            headers={'User-Agent': UserAgent().random}
        )
    else:
        prepared_text = search_text.replace(
            " ", "+"
        )  # аргумент запроса содержит плюсы вместо пробелов
        response = requests.get(
            f"https://datika.me/search/?query={prepared_text}",
            headers={'User-Agent': UserAgent().random}
        )

    if check_200_status(response.status_code):
        soup = BeautifulSoup(response.content, "html.parser")

        found = soup.find(class_='product-list products_view_grid')  # сетка продуктов
        if not found:
            return []

        items = found.find_all(attrs={"itemtype": "http://schema.org/Product", "itemscope": True})
        if not items:
            return []

        res = []
        for item in items:
            title = item.find(attrs={"itemprop": "name"})
            if title:
                title = title.text
                if title.lower().find(search_text.lower()) == -1:
                    continue
            else:
                continue
            price = item.find(class_='price nowrap')
            if price:
                price = price.text
            else:
                continue
            price = price.replace(',', '').replace(' ', '')
            price = float(re.search(r'\d+(?:\.\d+)?', price)[0])
            picture = 'https://datika.me' + item.find(attrs={"itemprop": "image"}).get('src')
            link = item.find('h5')
            link = 'https://datika.me' + link.find('a').get('href')
            res.append({'title': title, 'price': price, 'link': link, 'picture': picture})

        res.sort(key=lambda x: x['price'])
        return res


def parse_multicom(search_text, category: str = None):
    if category:
        response = requests.get(
            f"https://www.multicom.me/{CATEGORIES[category]['multicom']}/svi.html?pretraga={quote(search_text)}",
            headers={'User-Agent': UserAgent().random}
        )
    else:
        response = requests.get(
            f"https://www.multicom.me/Pretraga?pretraga={MulticomEncoder().encode(search_text)}",
            headers={'User-Agent': UserAgent().random}
        )

    soup = BeautifulSoup(response.content, 'html.parser')
    found = soup.find(class_='artikli d-flex row')

    if not found:
        return []

    items = found.find_all(class_=re.compile(r'artikal-n d-flex flex-column.+'))
    if not items:
        return []

    res = []
    for item in list(items)[1:]:
        elem_h2 = item.find('h2')
        if elem_h2:
            elem_a = elem_h2.find('a')
            title = elem_a.text
            if title.lower().find(search_text.lower()) == -1:
                continue
            link = 'https://www.multicom.me' + elem_a.get('href')
        else:
            continue

        price = item.find(class_='cijenaGotovina')
        if price:
            price = price.text
        else:
            continue
        price = float(re.search(r'\d+(?:\.\d+)?', price)[0])

        picture = item.find('img').get('src')

        res.append({'title': title, 'price': price, 'link': link, 'picture': picture})

    res.sort(key=lambda x: x['price'])
    return res