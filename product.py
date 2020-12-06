from typing import Dict, Union

import json


class Product:
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        value = ' '.join(value.strip().split())
        self.__name = value

    @property
    def price(self) -> int:
        return self.__price

    @price.setter
    def price(self, value: Union[int, str]):
        if isinstance(value, int):
            self.__price = value
        else:
            if not isinstance(value, str):
                value_type = value.__class__.__name__
                raise TypeError(f"{value_type} is invalid")

            value = ''.join(value.strip().split())
            if not value.isnumeric():
                raise ValueError("Can't convert value to int")

            self.__price = int(value)

    def __init__(self, name: str, price: str):
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f"{self.name} = {self.price}"

    def __repr__(self) -> str:
        return f"Product('{self.name}', {self.price})"


def encode_product(o: Product):
    if isinstance(o, Product):
        return {"name": o.name, "price": o.price}

    return json.JSONEncoder().default(o)


def decode_product(o: Dict[str, int]):
    return Product(o["name"], o["price"])
