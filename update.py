import json

from utils import search

def add_product(products, name, price):
    products[name] = price
    print("\n{} = {}\n".format(name, price))


if __name__ == "__main__":
    price_list_path = "price_list.json"

    with open(price_list_path, "r") as price_list:
        products = json.load(price_list)

    while True:
        command = input(">>> ")

        if command == "/done":
            break

        command = list(map(lambda str: str.strip(), command.split("=")))

        if len(command) == 1:
            print("Invalid command")
            continue

        name, price = command

        matched_product_names = search(name, products.keys())

        if len(matched_product_names) == 0:
            add_product(products, name, price)
        else:
            print("\nSimilar products:")
            for i, matched_name in enumerate(matched_product_names, 1):
                print("{}) {} = {}".format(
                    i, matched_name, products[matched_name]))
            print("n) Add new product")
            print("c) Skip")

            choice = input("Option: ").strip()
            choice = - \
                1 if choice == "c" else 0 if choice == "n" else int(choice)

            if choice == 0:
                add_product(products, name, price)
            elif choice != -1:
                old_product_name = matched_product_names[choice - 1]
                add_product(products, old_product_name, price)

    with open(price_list_path, "w") as price_list:
        json.dump(products, price_list)
