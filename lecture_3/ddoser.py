from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from faker import Faker
import random

# Initialize Faker for generating fake data
faker = Faker()

# Base URL for API
BASE_URL = "http://localhost:8080"

# Functions to interact with the `cart` and `item` endpoints

def create_cart():
    response = requests.post(f"{BASE_URL}/cart")
    print(f"Create Cart: {response.status_code}, {response.json()}")
    return response.json().get("id")

def get_cart(cart_id):
    response = requests.get(f"{BASE_URL}/cart/{cart_id}")
    print(f"Get Cart {cart_id}: {response.status_code}, {response.json()}")

def list_carts():
    params = {
        "offset": random.randint(0, 5),
        "limit": random.randint(5, 15),
        "min_price": round(random.uniform(5, 50), 2),
        "max_price": round(random.uniform(50, 100), 2),
        "min_quantity": random.randint(0, 10),
        "max_quantity": random.randint(10, 20)
    }
    response = requests.get(f"{BASE_URL}/cart", params=params)
    print(f"List Carts: {response.status_code}, {response.json()}")

def add_item_to_cart(cart_id, item_id):
    response = requests.post(f"{BASE_URL}/cart/{cart_id}/add/{item_id}")
    print(f"Add Item {item_id} to Cart {cart_id}: {response.status_code}, {response.json()}")

def create_item():
    item_data = {
        "name": faker.word(),
        "price": round(random.uniform(10, 100), 2),
        "quantity": random.randint(1, 20)
    }
    response = requests.post(f"{BASE_URL}/item", json=item_data)
    print(f"Create Item: {response.status_code}, {response.json()}")
    return response.json().get("id")

def get_item(item_id):
    response = requests.get(f"{BASE_URL}/item/{item_id}")
    print(f"Get Item {item_id}: {response.status_code}, {response.json()}")

def list_items():
    params = {
        "offset": random.randint(0, 5),
        "limit": random.randint(5, 15),
        "min_price": round(random.uniform(10, 50), 2),
        "max_price": round(random.uniform(50, 100), 2),
        "show_deleted": random.choice([True, False])
    }
    response = requests.get(f"{BASE_URL}/item", params=params)
    print(f"List Items: {response.status_code}, {response.json()}")

def update_item(item_id):
    updated_data = {
        "name": faker.word(),
        "price": round(random.uniform(10, 100), 2),
        "quantity": random.randint(1, 20)
    }
    response = requests.put(f"{BASE_URL}/item/{item_id}", json=updated_data)
    print(f"Update Item {item_id}: {response.status_code}, {response.json()}")

def patch_item(item_id):
    patch_data = {"price": round(random.uniform(5, 75), 2)}
    response = requests.patch(f"{BASE_URL}/item/{item_id}", json=patch_data)
    print(f"Patch Item {item_id}: {response.status_code}, {response.json()}")

def delete_item(item_id):
    response = requests.delete(f"{BASE_URL}/item/{item_id}")
    print(f"Delete Item {item_id}: {response.status_code}, {response.json()}")

# Running requests concurrently

with ThreadPoolExecutor() as executor:
    futures = []

    # Create carts and items
    for _ in range(10):
        futures.append(executor.submit(create_cart))
        futures.append(executor.submit(create_item))

    # Use created cart and item IDs for further requests
    cart_ids = [future.result() for future in futures if future.result()]
    item_ids = cart_ids[:len(cart_ids)//2]  # Some item IDs

    # Fetch details and perform actions on items and carts
    for cart_id in cart_ids:
        futures.append(executor.submit(get_cart, cart_id))
        futures.append(executor.submit(list_carts))
        
        for item_id in item_ids:
            futures.append(executor.submit(add_item_to_cart, cart_id, item_id))

    for item_id in item_ids:
        futures.append(executor.submit(get_item, item_id))
        futures.append(executor.submit(list_items))
        futures.append(executor.submit(update_item, item_id))
        futures.append(executor.submit(patch_item, item_id))
        futures.append(executor.submit(delete_item, item_id))

    # Wait for all requests to complete
    for future in as_completed(futures):
        print(f"Completed: {future}")
