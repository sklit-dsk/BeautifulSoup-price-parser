from bs4 import BeautifulSoup
import requests
import re

MAX_ITEMS = 10


def handle_data(parsed_data: list, source: str):
    if parsed_data:
        print(parsed_data)
    else:
        print(f'Не удалось получить данные со страницы. Источник "{source}"')


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

        pattern = re.compile(r"fnc-product-name-\d+")
        found = soup.find_all(id=pattern)

        return [x.text.replace("\n", "") for x in found[:MAX_ITEMS]]


search_text = 'iphone 14 256'
parsed_data = parse_tehnomax(search_text)
handle_data(parsed_data, "tehnomax")
