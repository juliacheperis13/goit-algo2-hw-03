import csv
import timeit
from BTrees.OOBTree import OOBTree


# Функція для завантаження товарів з CSV
def load_items(filename):
    items = []
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            item = {
                "ID": int(row["ID"]),
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"]),
            }
            items.append(item)
    return items


# Функція для додавання товару в OOBTree
def add_item_to_tree(tree, item):
    tree[item["ID"]] = item


# Функція для додавання товару в dict
def add_item_to_dict(d, item):
    d[item["ID"]] = item


# Функція для виконання діапазонного запиту для OOBTree
def range_query_tree(tree, min_price, max_price):
    return [
        item
        for item in tree.items(min_price, max_price)
        if min_price <= item[1]["Price"] <= max_price
    ]


# Функція для виконання діапазонного запиту для dict
def range_query_dict(d, min_price, max_price):
    return [item for item in d.values() if min_price <= item["Price"] <= max_price]


# Основна частина програми
def main():
    items = load_items("generated_items_data.csv")

    tree = OOBTree()
    d = {}

    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(d, item)

    # Визначення діапазону цін
    min_price = 10.0
    max_price = 50.0

    # Функція для вимірювання часу
    def time_query(func, *args):
        return timeit.timeit(lambda: func(*args), number=100)

    # Вимірювання часу для OOBTree
    total_time_tree = time_query(range_query_tree, tree, min_price, max_price)
    print(f"Total range_query time for OOBTree: {total_time_tree:.6f} seconds")

    # Вимірювання часу для dict
    total_time_dict = time_query(range_query_dict, d, min_price, max_price)
    print(f"Total range_query time for Dict: {total_time_dict:.6f} seconds")


if __name__ == "__main__":
    main()


# Total range_query time for OOBTree: 0.000349 seconds
# Total range_query time for Dict: 0.303336 seconds