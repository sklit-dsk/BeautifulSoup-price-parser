from bs4 import BeautifulSoup
import requests


def parse_page(url):
    # Отправляем GET запрос к странице
    response = requests.get(f"https://pc-gamer.me/pretraga/?q={url}")

    # Проверяем, что запрос успешен (status code 200)
    if response.status_code == 200:
        # Используем BeautifulSoup для парсинга HTML контента
        soup = BeautifulSoup(response.content, "html.parser")

        # Находим все элементы с определенным классом
        elements_with_class_names = soup.find_all(class_="fh-5 fw-700 text-black")
        elements_with_class_prices = soup.find_all(class_="fh-4 fw-800 text-white")

        # Возвращаем текстовое содержимое найденных элементов
        print([element.text for element in elements_with_class_prices])
        return [element.text for element in elements_with_class_names]
    else:
        print("Ошибка при получении страницы:", response.status_code)
        return None


# Пример использования
# Задаем URL страницы для парсинга
url = input("Enter the product: ")

# Парсим страницу
parsed_data = parse_page(url)

# Выводим результат
if parsed_data:
    print(parsed_data)
else:
    print("Не удалось получить данные с страницы.")
