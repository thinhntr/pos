from typing import Dict, Union

import json


class Product:
    """
    Product's information
    """

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        """Set product's name

        Raises
        ------
        ValueError
            If `value` is an empty string
        """
        value = " ".join(value.strip().split())
        if value == "":
            raise ValueError("Product's name can't be an empty string")
        self.__name = value
        return True

    @property
    def price(self) -> int:
        return self.__price

    @price.setter
    def price(self, value: int):
        """Set product's price

        Raises
        ------
        ValueError
            If `value` is less than 0
        """
        if value < 0:
            raise ValueError(f"Product's price can't be less than 0 ({value} < 0)")
        self.__price = value

    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f"{self.name} = {self.price}"

    def __repr__(self) -> str:
        return f"Product('{self.name}', {self.price})"


def encode_product(o):
    if isinstance(o, Product):
        return {"name": o.name, "price": o.price}

    return json.JSONEncoder().default(o)


def decode_product(o):
    return Product(o["name"], o["price"])
