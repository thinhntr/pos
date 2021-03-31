# Products' prices manager

An app to manage products' prices written in python

## Install dependencies

`pip install -r requirements.txt`

## How to use

### Run the main app

`python main.py`

### Commands

- `/help`: Display all commands
- `/exit`: Quit program
- `/clrscr`: Clear all information displayed on screen
- `/save`: Save all products' info to price_list.json
- `/all`: Show all products

![](https://imgur.com/w05LPsB.png)

- `/del`: Show a prompt to delete a product by its index

![](https://imgur.com/SMyGc0G.png)

- `index`: Show a prompt to modify  information about product at `index` (`index` can be 1, 2, 3, ...)

![](https://imgur.com/o2hgCZ6.png)

- `[query name]`: Search for products with similar name

![](https://imgur.com/qMo7a2Q.png)

- `[product name] = [price]`: Add a product with its price to the database

![](https://imgur.com/RjA585x.png)

## For development

Install mypy and black: `pip install mypy black`

- main.py: Main app
- product.py: Contain `Product` class to store names and prices
- product_manager.py: Manage list of products
- utils.py: misc. tools
- price_list.json: product's prices database
