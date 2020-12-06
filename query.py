import json
from utils import search

if __name__ == "__main__":
    price_list_path = "price_list.json"

    with open(price_list_path, "r") as price_list:
        products = json.load(price_list)

    while True:
        query = input(">>> ").strip()

        if query == '/done':
            break

        for name in search(query, products.keys()):
            print("{} = {}".format(name, products[name]))
