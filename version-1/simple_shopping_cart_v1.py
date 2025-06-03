# Simple shopping cart program version 1

import json
import os
from datetime import datetime

# Defining variables

MAX_PRICE = 10000
MIN_PRICE = 0

MIN_QUANTITY = 0
MAX_QUANTITY = 100

# Get the directory where the script is located. Did this because it kept on making file in wrong place for some reason.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Create json file if it doesn't exist
USERS_FILE = os.path.join(SCRIPT_DIR, "users.json")
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f, indent=4)  # Added indent=4 for nicer looking JSON file

def login_user():
    print("\n=== Welcome to the Simple Shopping Cart System ===")
    while True:
        username = input("Enter your username: ").strip().lower()
        if username:  # Checking if username is not empty after stripping
            break
        print("Username cannot be blank. Please try again.")
    
    # Load user data from json file
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    # If the username is in the list of users
    if username in users:
        print(f"\nWelcome back, {username}")
        cart = users[username]["cart"]
    else:
        # Create new user entry if it is a new user
        users[username] = {
            "joined_date": datetime.now().strftime("%Y-%m-%d"),
            "cart": {}
        }
        cart = {}
        # Save new user
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)
        print(f"\nWelcome, new user {username}")
    
    return username, cart

# Save cart function
def save_cart(username, cart):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    
    users[username]["cart"] = cart
    
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Show main menu function
def show_menu():
    print("\n=== Simple Shopping Cart Menu ===")
    print("1. Add item")
    print("2. Remove item")
    print("3. View cart and total")
    print("4. Exit")

# Add item to cart function
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
            # If item exists, show current price
            if item in cart:
                current_price = cart[item]["price"]
                print(f"Item already in cart at ${current_price:.2f} per item.")
                use_current = input("Use current price? (y/n): ").lower().strip()
                if use_current == 'y':
                    price = current_price # Uses current price and breaks loop
                    break
            
            price = float(input("Enter item price: $"))
            if price <= MIN_PRICE:
                print("Price must be greater than $0. Please try again.")
                continue
            if price > MAX_PRICE:
                print("Price is too high. Maximum price allowed is $10,000. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid price. Please enter a valid number.")

    # Get and validate quantity
    while True:
        try:
            # If item exists, show current quantity, then choose quantity to add ontop of current quantity
            current_quantity = cart[item]["quantity"] if item in cart else 0
            quantity = int(input(f"Enter quantity to add (current: {current_quantity}): "))
            
            if quantity <= MIN_QUANTITY:
                print("Quantity must be greater than 0. Please try again.")
                continue
                
            new_quantity = current_quantity + quantity
            if new_quantity > MAX_QUANTITY:
                print(f"Total quantity would exceed 100 (current: {current_quantity}, adding: {quantity})")
                print("Please enter a smaller quantity.")
                continue
            break
        except ValueError:
            print("Invalid quantity. Please enter a whole number.")

    # Update or add item to cart
    if item in cart:
        cart[item]["quantity"] += quantity
        if price != cart[item]["price"]:
            cart[item]["price"] = price
            print(f"\nUpdated {item} price to ${price:.2f}")
        print(f"Added {quantity} more {item}(s) to cart (new total: {cart[item]['quantity']})")
    else:
        cart[item] = {"price": price, "quantity": quantity}
        print(f"\n{quantity} {item}(s) added to cart")

def remove_item(cart):
    if not cart:
        print("\nCart is empty!")
        return
    print("\nItems in cart:")
    # For loop to print stuff in cart.
    for item in cart:
        print(f"- {item}")
    item = input("Enter item to remove: ")
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
    
    print("\n" + "="*40) # Print 40 = signs to make it look nice
    print(f"Total: ${total:.2f}")

# Main function to call other functions and run the program.
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