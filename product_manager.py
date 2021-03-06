import json
import os
from typing import Iterable, List, Optional, Tuple

from fuzzywuzzy import fuzz
from unidecode import unidecode

from product import Product, decode_product, encode_product
from utils import construct_poll, dp_lcs, get_choice, rlinput, to_valid_price

DEFAULT_PRICELIST_PATH = "./price_list.json"


class ProductManager:
    """
    Create an object to manage products

    Attributes
    ----------
    count
    products : List[Product]
        List of all products' information
    """

    @property
    def count(self) -> int:
        """
        Number of products in the current database
        """
        return len(self.products)

    def __init__(self, database_filename: Optional[str] = None):
        self.products: List[Product] = []

        if database_filename is not None:
            self.load_from_file(database_filename)
        elif os.path.exists(DEFAULT_PRICELIST_PATH):
            self.load_from_file()

    def get_products(self, indices: Optional[Iterable[int]] = None) -> List[Product]:
        if indices is None:
            indices = range(self.count)

        return [self.products[i] for i in indices]

    def search(self, keyword: str) -> List[int]:
        """Search for product with name similar to `keyword`
        """
        candidates: List[Tuple[int, int, int]] = []

        for i in range(self.count):
            product_name = self.products[i].name

            # Similarity score between `keyword` and `product_name`
            # when converting both of them into ascii chars
            score1 = fuzz.token_set_ratio(unidecode(keyword), unidecode(product_name))

            # Similarity score between `keyword` and `product_name`
            # when not converting them ino ascii chars
            score2 = fuzz.token_set_ratio(keyword, product_name, force_ascii=False)

            if score1 >= 50 or score2 >= 50:
                candidate = (score1 * score2, score1, i)
                candidates.append(candidate)

        candidates.sort(key=lambda e: e[:2], reverse=True)

        if len(candidates) > 0:
            max_score1 = candidates[0][1]

            return [
                candidates[i][-1]
                for i in range(len(candidates))
                if max_score1 - candidates[i][1] <= 20
            ]
        
        return []

    def add_product(self, name: str, price: int):
        """Add product to the database"""
        similar_product_indices = self.search(name)

        if len(similar_product_indices) == 0:
            self.products.append(Product(name, price))
            return

        similar_products = self.get_products(similar_product_indices)
        similar_product_names = list(map(lambda p: p.name, similar_products))
        choices = construct_poll(
            [*similar_product_indices, "n"],
            [*similar_product_names, "Add as new product"],
        )

        choice = get_choice(choices, "Similar products")

        if choice == "n":
            self.products.append(Product(name, price))
        elif isinstance(choice, int):
            self.modify_product(choice, name, price)
        else:
            print("Skipped")

    def modify_product(
        self, index: int, new_name: str = "", new_price: Optional[int] = None
    ):
        if not isinstance(index, int):
            print(f"Invalid index ({index})")
            return

        if not (0 <= index and index < self.count):
            print(f"Index out of range ({index})")
            return

        print(f"Chosen product: {self.products[index]}")

        choices = [
            ("r", "Update name"),
            ("p", "Update price"),
            ("b", "Update name and price"),
            ("d", "Delete this product"),
        ]
        choice = get_choice(choices)

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

    def change_product_price(self, index: int, new_price: Optional[int] = None):
        """
        Change product's price at index
        """
        while new_price is None:
            try:
                new_price = to_valid_price(
                    rlinput("New price: ", str(self.products[index].price))
                )
            except RuntimeError:
                continue
            else:
                break

        self.products[index].price = new_price

    def delete(self):
        """
        CLI for remove function
        """
        index = input("Enter product's index: ").strip()
        if not index.isnumeric():
            print("Invalid index")

        confirm_delete = input("Do you want to continue? [Y/n] ").strip().lower() == "y"
        if confirm_delete:
            self.remove(int(index))

    def remove(self, index: int):
        """
        Remove product at index
        """
        self.products.pop(index)

    def show(self, indices: Optional[Iterable[int]] = None, nameonly: bool = False):
        """
        Print products at indices.
        If indices is None then print all products available

        Parameters
        ----------
        nameonly : bool
            If nameonly is False then print product's name and price
        """
        if indices is None:
            indices = range(self.count)

        for index in indices:
            result = self.products[index].name if nameonly else self.products[index]
            print(f"    {index}) {result}")

    def load_from_file(self, filename: str = DEFAULT_PRICELIST_PATH):
        """
        Load products' information from `filename` to this instance
        """
        try:
            with open(filename, "r") as price_list:
                self.products = json.load(price_list, object_hook=decode_product)
                print(f"Data loaded from {filename}")
        except FileNotFoundError:
            choices = construct_poll(["y", "n"], [f"Create {filename}", "Abort"])

            choice = get_choice(choices)

            if choice == "y":
                self.save_to_file(filename)

    def save_to_file(self, filename: str = DEFAULT_PRICELIST_PATH):
        """
        Save products' information from this instance to `filename`
        """
        with open(filename, "w") as price_list:
            json.dump(self.products, price_list, default=encode_product, indent=2)
            print(f"Data saved to {filename}")
