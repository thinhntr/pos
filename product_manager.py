from typing import List, Optional, Union

import json

from utils import dp_lcs
from utils import get_choice
from utils import rlinput
from product import Product
from product import encode_product, decode_product


class ProductManager:
    @property
    def count(self) -> int:
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
            return [i for i in range(self.count) if lengths[i] == max_len]

        return [[i, self.products[i].name] for i in range(self.count) if lengths[i] == max_len]

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

    def modify_product(self, index: int, new_name="", new_price=""):
        if not isinstance(index, int):
            print("Invalid index")
            return

        if not (0 <= index and index < self.count):
            print("index out of range")
            return
        print(f"Chosen product: {self.products[index]}")
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

    def change_product_name(self, index: int, new_name: str = ""):
        """
        Change product's name at index
        """
        while new_name == "":
            new_name = rlinput("New name: ", self.products[index].name)
        
        self.products[index].name = new_name

    def change_product_price(self, index: int, new_price: int = ""):
        """
        Change product's price at index
        """
        while new_price == "":
            new_price = rlinput("New price: ", self.products[index].price)
        
        self.products[index].price = new_price

    def delete(self):
        """
        CLI for remove function
        """
        index = input("Enter product's index: ").strip()
        if not index.isnumeric():
            print("Invalid index")
        else:
            self.remove(int(index))

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
            indices = range(self.count)

        for index in indices:
            result = self.products[index].name if nameonly else self.products[index]
            print(f"    {index}) {result}")

    def load_from_file(self, filename: str = "price_list.json"):
        try:
            with open(filename, "r") as price_list:
                self.products = json.load(
                    price_list, object_hook=decode_product)
                print(f'Data loaded from {filename}')
        except FileNotFoundError:
            self.save_to_file(filename)

    def save_to_file(self, filename: str = "price_list.json"):
        self.products.sort(key=lambda p: (p.name, p.price))
        
        with open(filename, "w") as price_list:
            json.dump(self.products, price_list, default=encode_product)
            print(f'Data saved to {filename}')
