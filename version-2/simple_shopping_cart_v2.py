# Simple shopping cart program version 2. This file is the main program that runs the shopping cart system along with the GUI, while the other shopping_cart.py file is more for the barebones of this code, if that makes sense.

# Importing modules
import os
import bcrypt
# I imported easygui as eg instead of doing from easygui import* because I wanted to make it easier to see which functions are from easygui.
import easygui as eg
from database import Database
from shopping_cart import ShoppingCart
from config import*


class ShoppingCartGUI:
    def __init__(self):
        """Initialize the shopping cart database, cart and user for this session."""
        self.db = Database(DB_FILE) # Initializes the database connection using the variable from config.py and the class in database.py.
        self.cart = None
        self.current_user = None

    def start(self):
        """Start the shopping cart program."""
        eg.msgbox("Welcome to the Simple Shopping Cart System V2", "Shopping Cart")
        while True: # This while loop keeps on running until the user chooses to exit.
            if not self.current_user: # If no user is logged in, show authentication menu
                self._show_auth_menu()
            else:
                self._show_main_menu()

    # I put an underscore before the name of most functions to show that they are internal methods/functions. This is because they are only called from inside the class.
    def _show_auth_menu(self):
        """Show the authentication menu for user to login or register a new account."""
        choices = ["Login", "Register", "Exit"]
        choice = eg.buttonbox("Please select an option:", "Authentication", choices)
        
        if choice == "Login":
            self._login()
        elif choice == "Register":
            self._register()
        elif choice == "Exit":
            if eg.ynbox("Are you sure you want to exit?", "Exit"):
                self.db.close() # Closes the database connection before exiting
                exit()
                
    def _login(self):
        """Handle user login."""
        attempts = 0
        while attempts < MAX_LOGIN_ATTEMPTS:
            fields = ["Username", "Password"]
            values = eg.multpasswordbox(
                f"Enter your login details:\n\nAttempts remaining: {MAX_LOGIN_ATTEMPTS - attempts}",
                "Login", 
                fields
            )
            
            if not values:  # User clicked Cancel
                return
                
            username, password = values # Unpacking values.
            username = username.strip().lower()
            user = self.db.get_user(username) # Calls get_user function from the Database class to get user data from the database.
            
            # Successfully logged in if user exists and password matches, user[1] is the same as password as the function returns a list
            if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
                # Initializing the current user and cart
                self.current_user = username
                self.cart = ShoppingCart()
                # Retrieves the items dictionary from the database for the current user, and sets it to self.items, which is accessed through self.cart.items
                self.cart.items = self.db.get_cart(username)
                eg.msgbox(f"Welcome back, {username}", "Login Successful")
                # Returning shows the main menu
                return
            
            attempts += 1
            if attempts < MAX_LOGIN_ATTEMPTS:
                eg.msgbox(f"Invalid username or password.\n\n{MAX_LOGIN_ATTEMPTS - attempts} attempts remaining.", 
                         "Login Failed")
            else:
                eg.msgbox("Maximum login attempts exceeded. Please try again later.", 
                         "Login Failed")

    def _register(self):
        """Handle user registration with proper password hiding."""
        # First get username
        username = eg.enterbox("Enter username:", "Register")
        if not username:
            return
            
        username = username.strip().lower()
        
        # Username validation
        if not username or len(username.strip()) == 0:
            eg.msgbox("Username cannot be empty or just spaces.", "Error")
            return
        
        if not username.isalnum():
            eg.msgbox("Username can only contain letters and numbers.", "Error")
            return
            
        if len(username) > MAX_USERNAME_LENGTH:
            eg.msgbox(f"Username must be {MAX_USERNAME_LENGTH} characters or less.", "Error")
            return
            
        if self.db.get_user(username): # If function returns something
            eg.msgbox("Username already exists.", "Error")
            return
        
        # Then get passwords separately with the passwordbox function that hides the password
        password = eg.passwordbox("Enter password:", "Register")
        if not password:
            return
            
        confirm = eg.passwordbox("Confirm password:", "Register")
        if not confirm:
            return
        
        # Password validation
        if password != confirm:
            eg.msgbox("Passwords do not match.", "Error")
            return
            
        if len(password) < MIN_PASSWORD_LENGTH:
            eg.msgbox(f"Password must be at least {MIN_PASSWORD_LENGTH} characters.", "Error")
            return
        
        # Hashing the password using bcrypt
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        if self.db.add_user(username, hashed):
            # If user and password is successfully added, sets the current user to the inputted username, and the current cart to
            self.current_user = username
            self.cart = ShoppingCart()
            eg.msgbox("Registration successful!", "Success")
            # After registration, it shows the main menu as the current user is now logged in.
        else:
            eg.msgbox("Registration failed. Please try again.", "Error")

    def _show_main_menu(self):
        """Show the main menu for the shopping cart functions."""
        while True:
            choices = ["Add Item", "Remove Item", "View Cart", "Clear Cart", "Logout"]
            choice = eg.buttonbox(
                "Select an option:",
                "Shopping Cart",
                choices
            )
            
            # If user selects one of the choices, calls the corresponding function. This is not to be confused with the functions in the ShoppingCart class in shopping_cart.py.
            if choice == "Add Item":
                self._add_item()
            elif choice == "Remove Item":
                self._remove_item()
            elif choice == "View Cart":
                self._view_cart()
            elif choice == "Clear Cart":
                self._clear_cart()
            elif choice == "Logout":
                if eg.ynbox("Are you sure you want to logout?", "Logout"):
                    self.current_user = None # Sets the currents user and cart to none for this session, so another user can log back in straight away. This works because once the current user is set to None, the program will return to the authentication menu because of the while loop in the _start() function.
                    self.cart = None # Closes the ShoppingCart instance, so a new user can create a new instance with their own cart.
                    return
                
    def _add_item(self):
        """Add an item to the cart."""
        fields = ["Item Name", "Price ($)", "Quantity"]
        values = eg.multenterbox("Enter item details:", "Add Item", fields)
        
        if values:
            name, price, quantity = values
            name = name.strip()
            
            try:
                price = float(price)
                quantity = int(quantity)
                
                # Validating the inputs
                if not name:
                    eg.msgbox("Item name cannot be blank.", "Error")
                    return
                    # Returns the user to the main menu instead of the same page, which may be annoying, but i will fix this in my next version.
                    
                if len(name) > MAX_ITEM_NAME_LENGTH:
                    eg.msgbox(f"Item name must be {MAX_ITEM_NAME_LENGTH} characters or less.", "Error")
                    return
                    
                if price <= 0:
                    eg.msgbox("Price must be greater than $0.", "Error")
                    return
                    
                if price > MAX_PRICE:
                    eg.msgbox(f"Price cannot exceed ${MAX_PRICE:,.2f}", "Error")
                    return
                    
                if quantity <= 0:
                    eg.msgbox("Quantity must be greater than 0.", "Error")
                    return
                    
                if quantity > MAX_QUANTITY:
                    eg.msgbox(f"Quantity cannot exceed {MAX_QUANTITY}", "Error")
                    return

                # Check if item already exists in cart
                cart_items = self.cart.get_items()
                # If item already exists in the cart, it updates the quantity instead of adding a new item.
                if name in cart_items:
                    current_quantity = cart_items[name]["quantity"]
                    # Adds the new quantity to the current quantity in the cart.
                    new_quantity = current_quantity + quantity
                    
                    # If the new quantity exceeds the maximum quantity, shows an error message and returns.
                    if new_quantity > MAX_QUANTITY:
                        eg.msgbox(f"Cannot add {quantity} more {name}(s). The total quantity would exceed {MAX_QUANTITY}.", "Error")
                        return
                    
                    # Updates the quantity of the item in the cart and database. Calls this function from the ShoppingCart class in shopping_cart.py.
                    self.cart.update_quantity(name, new_quantity)
                    # Calls the get_items() function from the ShoppingCart class in shopping_cart.py to get the items in the cart, it doesn't call the function get_cart() in database.py.
                    self.db.update_cart(self.current_user, self.cart.get_items())
                    eg.msgbox(f"Added {quantity} more {name}(s) to cart.\nNew quantity: {new_quantity}", "Success")
                # Else it just adds the items to the cart.
                else:
                    self.cart.add_item(name, price, quantity)
                    self.db.update_cart(self.current_user, self.cart.get_items())
                    eg.msgbox(f"{quantity} {name}(s) added to cart", "Success")
                
            except ValueError:
                eg.msgbox("Invalid price or quantity.", "Error")

    def _remove_item(self):
        """Remove an item from the cart."""
        # If the cart is empty, shows error message then returns to main menu
        if self.cart.is_empty():
            eg.msgbox("Cart is empty.", "Error")
            return
        # Extracts the item names from the self.items dictionary
        items = list(self.cart.get_items().keys())
        
        # If there's only one item, ask directly if user wants to remove it
        if len(items) == 1:
            item = items[0]
            # Asks the user if they want to remove item from the cart, which continues if returned as True. I should probably add a feature where it allows the user to just remove a specific quantity.
            if eg.ynbox(f"Do you want to remove {item}?", "Remove Item"):
                # Removes item from cart and database.
                self.cart.remove_item(item)
                self.db.update_cart(self.current_user, self.cart.get_items()) # This takes the temporary cart from self.cart.items and updates the database with it.
                eg.msgbox(f"{item} removed from cart", "Success")
            return
            
        # If there are multiple items, show choice box to select item to remove
        choice = eg.choicebox("Select an item to remove from your cart:", "Remove Item", items)
        if choice and eg.ynbox(f"Are you sure you want to remove {choice}?", "Confirm"): # Once again, I should add an option to just remove a specific quantity, but I will add that in my next version.
            # If this choice is returned True, continues to remove the item from the cart and database.
            self.cart.remove_item(choice) # Removes the choice from self.items.
            self.db.update_cart(self.current_user, self.cart.get_items()) # Like the previous section, this takes the temporary cart from self.cart.items and updates the database with it.
            eg.msgbox(f"{choice} removed from cart", "Success")
            
    def _view_cart(self):
        """View cart contents and total."""
        if self.cart.is_empty():
            eg.msgbox("Cart is empty", "Cart")
            return
        
        text = "=== Your Cart ===\n\n"
        for item, details in self.cart.get_items().items(): # .items returns the self.items dictionary as key value pairs, where item is the key and details is the value, which is a dictionary with price and quantity.
            subtotal = details["price"] * details["quantity"] # Square brackets are used to access the price and quantity from the dictionary.
            text += f"{item}: ${details['price']:.2f} x {details['quantity']} = ${subtotal:.2f}\n"
        
        text += f"\nTotal: ${self.cart.get_total():.2f}"
        eg.textbox("Cart Contents", "View Cart", text)

    def _clear_cart(self):
        """Clear all items from the cart."""
        if self.cart.is_empty():
            eg.msgbox("Cart is already empty", "Cart")
            return
        
        if eg.ynbox("Are you sure you want to clear your cart?", "Confirm"): # If returned as True, continues to clear the cart.
            self.cart.clear() # Clears the temporary cart in self.items
            self.db.update_cart(self.current_user, self.cart.get_items()) # Updates the database with the new temporary cart, which is now empty.
            eg.msgbox("Cart cleared successfully", "Success")

def main():
    app = ShoppingCartGUI()
    app.start()

if __name__ == "__main__":
    main()