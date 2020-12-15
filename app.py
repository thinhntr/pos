from product_manager import ProductManager
from utils import is_not_valid_input, clrscr, to_valid_price

if __name__ == "__main__":
    clrscr()

    product_manager = ProductManager()

    while True:
        command = input(">>> ").strip()

        if command == "/exit":
            break

        if command == "/clrscr":
            clrscr()

        elif command == "/help":
            print("/help: Display this help menu")
            print("/exit: Quit program")
            print("/clrscr: Clear screen")
            print("/all: Show all products")
            print("/del: Delete a product")
            print("/save: Save all products down to hardrive")
            print("[index]: Display information about product at index")
            print("[query_name]: Search products with similar name")
            print("[product_name]=[product_price]: Add product")

        elif command == "/all":
            product_manager.show()

        elif command == "/del":
            product_manager.delete()

        elif command.isnumeric():
            index = int(command)
            product_manager.modify_product(index)

        elif "=" in command:
            new_product = command.split("=")
            if len(new_product) != 2:
                print("Invalid command")
            else:
                name, price = new_product

                if is_not_valid_input(name):
                    print(f"Invalid name ({name})")
                    continue

                try:
                    new_price = to_valid_price(price)
                except RuntimeError:
                    print(f"Can't convert{price} to a valid value")
                    continue

                product_manager.add_product(name, new_price)

        elif command == "/save":
            product_manager.save_to_file(database_file_path)

        elif len(command) != 0:
            name = command
            product_manager.show(product_manager.search(command))

    product_manager.save_to_file(database_file_path)
