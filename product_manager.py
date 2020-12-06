import json
from typing import List, Optional, Union

from utils import dp_lcs
from utils import get_choice
from product import Product
from product import encode_product, decode_product


class ProductManager:
    @property
    def n_products(self) -> int:
        return len(self.products)

    def __init__(self):
        self.products: List[Product] = []

    def search(self, name: str, include_name_list: bool = False) -> Union[List[int], List[List]]:
        """
        Return products' indices with similar name.
        If include_name_list is True then return their corresponding names
        """
        name = name.lower()
        max_len = 0
        lengths: List[int] = []

        for product in self.products:
            current_len = dp_lcs(name, product.name.lower())
            lengths.append(current_len)
            max_len = max(max_len, current_len)

        if max_len == 0:
            return []

        if not include_name_list:
            return [i for i in range(self.n_products) if lengths[i] == max_len]

        return [[i, self.products[i].name] for i in range(self.n_products) if lengths[i] == max_len]

    def add_product(self, name: str, price: Union[int, str]):
        """
        Add product to the database"
        """
        matched_products = self.search(name, include_name_list=True)

        if len(matched_products) == 0:
            self.products.append(Product(name, price))

        else:
            options = [
                *matched_products,
                ["n", "Add as new product"]
            ]

            choice = get_choice(options, "Similar products")

            if choice == "n":
                self.products.append(Product(name, price))
            elif isinstance(choice,  int):
                self.modify_product(choice, name, price)
            else:
                print("Skipped")

    def modify_product(self, index, new_name, new_price):
        options = [
            ["r", "Update name"],
            ["p", "Update price"],
            ["b", "Update name and price"],
            ["d", "Delete this product"]
        ]
        choice = get_choice(options)

        if choice == "r":
            self.change_product_name(index, new_name)
        elif choice == "p":
            self.change_product_price(index, new_price)
        elif choice == "b":
            self.change_product_name(index, new_name)
            self.change_product_price(index, new_price)
        elif choice == "d":
            self.remove(index)
        else:
            print("Skipped")

    def change_product_name(self, index: int, new_name: str):
        """
        Change product's name at index
        """
        self.products[index].name = new_name

    def change_product_price(self, index: int, new_price: int):
        """
        Change product's price at index
        """
        self.products[index].price = new_price

    def remove(self, index: int):
        """
        Remove product at index
        """
        self.products.pop(index)

    def show(self, indices: Optional[List[int]] = None, nameonly=False):
        """
        Print products at indices.
        If indices is None then print all products available
        """
        if indices is None:
            indices = range(self.n_products)

        for index in indices:
            result = self.products[index].name if nameonly else self.products[index]
            print(f"{index}) {result}")

    def load_from_file(self, filename: str = "price_list.json"):
        with open(filename, "r") as price_list:
            self.products = json.load(price_list, object_hook=decode_product)

    def save_to_file(self, filename: str = "price_list.json"):
        with open(filename, "w") as price_list:
            json.dump(self.products, price_list, default=encode_product)
