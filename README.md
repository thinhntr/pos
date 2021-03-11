# Products' prices manager

## Install dependencies

`pip install -r requirements`

## How to use

### Run the main app

`python main.py`

### Commands

- `/help`: Display all commands
- `/exit`: Quit program
- `/clrscr`: Clear all information displayed on screen
- `/all`: Show all products
- `/del`: Show a prompt to delete a product by its index
- `/save`: Save all products' info to price_list.json
- `index`: Show a prompt to modify  information about product at `index` (`index` can be 1, 2, 3, ...)
- `query name`: Search for products with similar name
- `product name = price`: Add a product with its price to the database

## For development

Install mypy and black: `pip install mypy black`

- main.py: Main app
- product.py: Contain `Product` class to store names and prices
- product_manager.py: Manage list of products
- utils.py: misc. tools
- price_list.json: product's prices database
