from product_manager import ProductManager as PM
from utils import clrscr

if __name__ == "__main__":
    clrscr()

    database_file_path = 'price_list.json'
    products = PM()
    products.load_from_file(database_file_path)

    while True:
        command = input(">>> ").strip()

        if command == '/exit':
            break

        if command == '/clrscr':
            clrscr()

        elif command == '/all':
            products.show()

        elif command == '/del':
            products.delete()

        elif command.isnumeric():
            index = int(command)
            products.modify_product(index)

        elif '=' in command:
            new_product = command.split('=')
            if len(new_product) != 2:
                print("Invalid command")
            else:
                name, price = new_product
                products.add_product(name, price)

        elif command == '/save':
            products.save_to_file(database_file_path)

        elif len(command) != 0:
            name = command
            products.show(products.search(command))

    products.save_to_file(database_file_path)
