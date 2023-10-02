import random

import requests

ENDPOINT = "http://127.0.0.1:8000/ecommerce/v1/purchase_products"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTYyNzExNjIsInR5cCI6ImFjY2VzcyIsInVzZXJfaWQiOjEsImVtYWlsIjoiZmFkaUBmYWhhZGJhaWcuY29tIiwiZmlyc3RfbmFtZSI6Ik11aGFtbWFkIEZhaGFkIiwibGFzdF9uYW1lIjoiQmFpZyJ9.WIYYTtksZkqtbEmULUidGU3xSZbhk4sXdsim6mspwZ8"


def get_random_product_id():
    # Get random product id from 1 to 25
    return random.randint(1, 25)


def get_random_quantity():
    # Get random quantity from 1 to 10
    return random.randint(1, 2)


def dummy_sales_data():
    # Iterate over all days in the range
    for n in range(0, 2000):
        number_of_items = get_random_quantity()
        items = []
        for i in range(0, number_of_items):
            item = {
                "product_id": get_random_product_id(),
                "quantity": get_random_quantity(),
            }
            items.append(item)

        request_data = {"items": items}

        # Send the request
        headers = {"Authorization": f"Bearer {TOKEN}"}
        response = requests.post(ENDPOINT, json=request_data, headers=headers)


if __name__ == "__main__":
    dummy_sales_data()
