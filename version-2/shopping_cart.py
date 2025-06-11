# Simple shopping cart program V2. This fule does most of the code, while the other is more for the GUI.

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
