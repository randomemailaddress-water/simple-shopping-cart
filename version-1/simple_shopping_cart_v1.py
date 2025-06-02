# Simple shopping cart program version 1

import json
import os
from datetime import datetime

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Create users file if it doesn't exist
USERS_FILE = os.path.join(SCRIPT_DIR, "users.json")
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f, indent=4)  # Added indent=4 for nicer looking JSON

# Defining variables
def login_user():
    print("\n=== Welcome to Shopping Cart ===")
    while True:
        username = input("Enter your username: ").strip().lower()
        if username:  # Check if username is not empty after stripping
            break
        print("Username cannot be blank. Please try again.")
    
    # Load users data
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    
    if username in users:
        print(f"\nWelcome back, {username}!")
        cart = users[username]["cart"]
    else:
        # Create new user entry
        users[username] = {
            "joined_date": datetime.now().strftime("%Y-%m-%d"),
            "cart": {}
        }
        cart = {}
        # Save new user
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)  # Added indent=4 for prettier JSON
        print(f"\nWelcome, new user {username}!")
    
    return username, cart

def save_cart(username, cart):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    
    users[username]["cart"] = cart
    
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)  # Added indent=4 for prettier JSON

def show_menu():
    print("\n=== Simple Shopping Cart Menu ===")
    print("1. Add item")
    print("2. Remove item")
    print("3. View cart and total")
    print("4. Exit")

def add_item(cart):
    # Get and validate item name
    while True:
        item = input("Enter item name: ").strip()
        if not item:
            print("Item name cannot be blank. Please try again.")
            continue
        break

    # Get and validate price
    while True:
        try:
            price = float(input("Enter item price: $"))
            if price <= 0:
                print("Price must be greater than $0. Please try again.")
                continue
            if price > 10000:  # Reasonable maximum price limit
                print("Price seems too high. Maximum allowed is $10,000. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid price! Please enter a valid number.")

    # Get and validate quantity
    while True:
        try:
            quantity = int(input("Enter quantity: "))
            if quantity <= 0:
                print("Quantity must be greater than 0. Please try again.")
                continue
            if quantity > 100:  # Reasonable maximum quantity limit
                print("Quantity seems too high. Maximum allowed is 100. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid quantity! Please enter a whole number.")

    # Add validated item to cart
    cart[item] = {"price": price, "quantity": quantity}
    print(f"\n{quantity} {item}(s) added to cart")

def remove_item(cart):
    if not cart:
        print("\nCart is empty!")
        return
    print("\nItems in cart:")
    for item in cart:
        print(f"- {item}")
    item = input("Enter item name to remove: ")
    if item in cart:
        del cart[item]
        print(f"\n{item} removed from cart")
    else:
        print(f"\n{item} not found in cart")

def view_cart_and_total(cart):
    if not cart:
        print("\nCart is empty!")
        return
        
    print("\n=== Your Cart ===")
    total = 0
    for item, details in cart.items():
        subtotal = details['price'] * details['quantity']
        total += subtotal
        print(f"{item}: ${details['price']} x {details['quantity']} = ${subtotal:.2f}")
    
    print("\n" + "="*40)
    print(f"Total: ${total:.2f}")

def main():
    username, cart = login_user()
    
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            add_item(cart)
            save_cart(username, cart)
        elif choice == "2":
            remove_item(cart)
            save_cart(username, cart)
        elif choice == "3":
            view_cart_and_total(cart)
        elif choice == "4":
            save_cart(username, cart)
            print(f"\nGoodbye, {username}! Thank you for shopping!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()