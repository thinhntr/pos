import json
from typing import Iterable, List, Optional
from product import Product, decode_product, encode_product
from utils import construct_poll, dp_lcs, get_choice, rlinput, to_valid_price


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

    def get_products_names(self, indices: Optional[Iterable[int]]) -> List[str]:
        """
        Returns
        -------
        List[str]
            List of all products' names available if indices is None else
            list of all products' names at indices
        """
        if indices is None:
            return [product.name for product in self.products]

        return [self.products[i].name for i in indices]

    def get_products_prices(self, indices: Optional[Iterable[int]]) -> List[int]:
        """
        Returns
        -------
        List[str]
            List of all products' prices available if indices is None else
            list of all products' prices at indices
        """
        if indices is None:
            return [product.price for product in self.products]

        return [self.products[i].price for i in indices]

    def __init__(self):
        self.products: List[Product] = []

    def search(self, name: str) -> List[int]:
        """
        Return products' indices with similar name.
        If include_name_list is True then return their corresponding names
        """
        name = name.lower()
        max_len = 0
        lengths: List[int] = []

        for product in self.products:
            # FIXME: Change algorithm
            current_len = dp_lcs(name, product.name.lower())
            lengths.append(current_len)
            max_len = max(max_len, current_len)

        if max_len == 0:
            return []

        return [i for i in range(self.count) if lengths[i] == max_len]

    def add_product(self, name: str, price: int):
        """
        Add product to the database"
        """
        similar_product_indices = self.search(name)

        if len(similar_product_indices) == 0:
            self.products.append(Product(name, price))

        else:
            similar_product_names = self.get_products_names(similar_product_indices)
            choices = construct_poll(
                [*similar_product_indices, "n"], 
                [*similar_product_names, "Add as new product"]
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
        else:
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

    def load_from_file(self, filename: str = "price_list.json"):
        """
        Load products' information from `filename` to this instance
        """
        try:
            with open(filename, "r") as price_list:
                self.products = json.load(price_list, object_hook=decode_product)
                print(f"Data loaded from {filename}")
        except FileNotFoundError:
            print(f"{filename} created.")
            self.save_to_file(filename)

    def save_to_file(self, filename: str = "price_list.json"):
        """
        Save products' information from this instance to `filename`
        """
        self.products.sort(key=lambda p: (p.name, p.price))

        with open(filename, "w") as price_list:
            json.dump(self.products, price_list, default=encode_product)
            print(f"Data saved to {filename}")
