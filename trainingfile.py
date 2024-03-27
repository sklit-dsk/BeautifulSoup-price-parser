from bs4 import BeautifulSoup
import requests
import re

MAX_ITEMS = 10


def handle_data(parsed_data: list, source: str):
    if parsed_data:
        print(parsed_data)
    else:
        print(f'Не удалось получить данные со страницы. Источник "{source}"')


def link_product(part_of_product_in_link):
    return "https://pc-gamer.me" + part_of_product_in_link


def check_200_status(value: int):
    if value == 200:
        return True
    print("Ошибка при получении страницы:", value)
    return False


def parse_page(search_text):
    # Отправляем GET запрос к странице
    response = requests.get(f"https://pc-gamer.me/pretraga/?q={search_text}")

    # Проверяем, что запрос успешен (status code 200)
    if check_200_status(response.status_code):
        # Используем BeautifulSoup для парсинга HTML контента
        soup = BeautifulSoup(response.content, "html.parser")

        elements_with_class_names = soup.find_all(class_="fh-5 fw-700 text-black")
        elements_with_class_prices = soup.find_all(class_="fh-4 fw-800 text-white")
        div_elements = (
            soup.find("div", {"class": "container bg-white"})
            .find("div", {"class": "productsl-row mt-2"})
            .find("div", {"class": "row align-items-start bg-white"})
            .find("div", {"class": "col-12 pt-3"})
            .find("div", {"class": "productsl-cardlist"})
            .find("div", {"class": "row row-cols-2 row-cols-md-4 g-1 gy-2"})
            .find_all("div", {"class": "col"})
        )
        links = []
        for div in div_elements:
            a_elements = div.find_all("a", href=True)
            for a in a_elements:
                link = a["href"]
                if "p/" in link:
                    links.append(link)
        # for link in links:
        #     print(link_product(link))

        # all_elements = []
        # for element in elements_with_class_names:
        #     all_elements.append(element.text)
        #     for child in elements_with_class_prices:
        #         all_elements.append(child.text)
        #         break

        all_elements = list(
            zip(
                [element.text for element in elements_with_class_names],
                [child.text for child in elements_with_class_prices],
                [link_product(link) for link in links],
            )
        )
        # Возвращаем текстовое содержимое найденных элементов
        return [element for element in all_elements]


# Пример использования
# Задаем URL страницы для парсинга
search_text = input("Enter the product: ")

# Парсим страницу
parsed_data = parse_page(search_text)

# Выводим результат
handle_data(parsed_data, "pc-gamer")


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


parsed_data = parse_tehnomax(search_text)
handle_data(parsed_data, "tehnomax")
