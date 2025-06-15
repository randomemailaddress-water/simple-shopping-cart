# Simple shopping cart program V3. You are meant to run the other file name simple_shopping_cart_v3.py to run the program. This file is imported into that file, where it uses functions from here. This file is more for the barebones of the code while the other for the GUI and other features.

class ShoppingCart:
    def __init__(self):
        """Initialize an empty shopping cart."""
        self.items = {}
        # self.items is more of a temporary cart, as it is not saved to a database but rather kept track of during the user's session.
    
    def add_item(self, item_name, price, quantity):
        """Add an item to the cart."""
        # Adds an item to the self.items dicitonary in this format.
        self.items[item_name] = {"price": price, "quantity": quantity}
    
    def remove_item(self, item_name):
        """Remove an item from the cart."""
        if item_name in self.items:
            del self.items[item_name] # Deletes item_name parameter from self.items, which acts as a temporary cart.
            return True # Returns True if item was removed successfully.
        return False # Returns False if item was not found in the cart. However, I do not expect to encounter this error. I could delete this and it would still work.
    
    def update_quantity(self, item_name, quantity):
        """Update the quantity of an item in the cart."""
        if item_name in self.items:
            # Sets the quantity in self.items to the new quantity.
            self.items[item_name]["quantity"] = quantity
    
    def clear(self):
        """Clear all items from the cart."""
        self.items = {} # Sets self.items to an empty dictionary, effectively clearing the cart.
    
    def get_total(self):
        """Calculate the total price of all items in the cart."""
        return sum(
            details["price"] * details["quantity"]
            for details in self.items.values() # Loops through all items in self.items and multiplies the price by the quantity, then adds them all together to get the total price.
        )
    
    def is_empty(self):
        """Check if the cart is empty."""
        return len(self.items) == 0 # Returns if this statement is true or false.
    
    def get_items(self):
        """Get all items in the cart."""
        return self.items
    
    def remove_quantity(self, item_name, quantity_to_remove):
        """Remove specific quantity of an item from cart."""
        if item_name in self.items:
            current_qty = self.items[item_name]["quantity"]
            new_qty = current_qty - quantity_to_remove
            
            # If new quantity would be 0 or less, remove the whole item
            if new_qty <= 0:
                return self.remove_item(item_name)
            
            # Update quantity in temporary cart
            self.items[item_name]["quantity"] = new_qty
            return True
        return False
