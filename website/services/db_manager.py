import csv
import os


def read_csv():
    res = []

    file_path = os.path.abspath('services/products/datika.csv')

    with open(file_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            res.append(row)
    return res


def search_in_datika_db(search_text: str, category: str):
    data = read_csv()
    res = []
    for row in data:
        if search_text.lower() in row['product_name'].lower() and category == row['category']:
            structure = {'title': row['product_name'], 'price': float(row['product_price']), 'link': row['product_url'],
                         'picture': row['product_picture'], 'shop_name': 'datika'}
            res.append(structure)
    return res


